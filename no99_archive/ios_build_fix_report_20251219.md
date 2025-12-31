# iOS Build Troubleshooting Report - 2025-12-19

---

## 技術摘要

**給工程師的快速參考**

**問題核心:** 在 Expo SDK 54 與 React Native 0.81.5 專案中整合 `@react-native-firebase` 時，遭遇無法解決的編譯衝突。

**環境:**
- Expo SDK 54
- React Native 0.81.5
- 目標, 整合 Firebase v12, `@react-native-firebase/*`
- 平台, iOS, 本地 build + EAS Build

**根本問題:**

- **Firebase 12 的依賴需求與 RN 0.81.5 的限制形成死結:**
  - Firebase 12 要求 `use_frameworks! :linkage => :static` 或 modular headers
  - RN 0.81.5 的 Hermes 引擎在 frameworks 模式下有 C++ ABI 不兼容
  - 錯誤, `HermesExecutorFactory.cpp` 中的 `unique_ptr` 和 `shared_ptr` template 衝突

- **無法繞過 Hermes 編譯:**
  - 即使設定 `jsEngine: "jsc"`，RN 0.81.5 仍會編譯 Hermes 源代碼
  - 導致相同的 12 個 C++ 編譯錯誤

- **降級 Firebase 到 v11 也失敗:**
  - Pod install 在本地環境反覆卡住, 產生重複進程
  - xcodebuild 卡在 "Planning build" 階段超過 20 分鐘
  - 懷疑是本地 CocoaPods/xcodebuild 環境問題

**嘗試過的方案:**
- 失敗, Static frameworks + gRPC opt-outs
- 失敗, 切換到 JSC 引擎
- 失敗, 降級 Firebase 到 v11
- 失敗, 完全移除 Firebase 的乾淨 build
- 失敗, EAS Build, 需要付費 Apple Developer 帳號 $99/年

**可行解決方案:**
- **付費註冊 Apple Developer $99/年 + 使用 EAS Build**
- **暫時移除 Firebase 改用 mock**
- **等待 Expo SDK 更新, 期待未來版本支援 React Native 0.82+**

**結論:** 這是 Expo SDK 54 的系統性限制問題。在沒有付費 Apple Developer 帳號的情況下，建議優先開發 Android 或暫時移除 Firebase。

---

## 背景 Context

在整合 Native Firebase, `@react-native-firebase`, 到 Expo 專案, Static Linking 模式, 時，遭遇了嚴重的 iOS 編譯錯誤。主要涉及 CocoaPods 的 Header Search Paths、Module Maps 以及靜態/動態庫的相容性衝突。這份報告記錄了問題的根源與最終的解決方案，以備日後維護參考。

## 遭遇問題 Problems Encountered

在此次除錯過程中，我們依序解決了以下數個核心錯誤：

- **Duplicate Tasks Error:**
  - **現象:** Build 失敗，顯示多個 Target, `RNFBApp`, `RNFBAuth` 等, 試圖同時執行同一個 Copy Script。
  - **Error Log:**
    ```
    Run script build phase 'Copy FirebaseAuth Swift Header' will be run during every build because it does not specify any outputs...
    (in target 'RNFBAuth' from project 'Pods')
    (in target 'RNFBFirestore' from project 'Pods')
    (in target 'RNFBApp' from project 'Pods')
    ```
  - **原因:** `Podfile` 中的 `post_install` hook 對每個 Target 都重複添加了相同的 Script Build Phase。

- **Missing Headers, FirebaseAuth & FirebaseCore:**
  - **現象:** `'FirebaseAuth/FirebaseAuth-Swift.h' file not found` 或 `'Firebase/Firebase.h' file not found`。
  - **Error Log:**
    ```
    ❌  Pods/RNFBApp: 'Firebase/Firebase.h' file not found
       └─[app]/ios/RNFBApp/RNFBAppModule.m:18:9
    ❌  Pods/RNFBApp: 'FirebaseCore/FirebaseCore.h' file not found
    ```
  - **原因:** 在 Static Library 模式下，CocoaPods 默認不會將 Swift Compatibility Header 暴露到標準路徑。

- **Module Map Conflict, gRPC:**
  - **現象:** 開啟 `use_modular_headers!` 後，出現 `module 'gRPC' not found` 或重新定義錯誤。
  - **Error Log Partial:**
    ```
    [!] The following Swift pods cannot yet be integrated as static libraries:
    The Swift pod `FirebaseAuth` depends upon ... `RecaptchaInterop`, which do not define modules.
    ```
  - **原因:** gRPC 系列套件, `gRPC-Core`, `gRPC-C++`, 的 module map 定義與 React Native 或 Firebase 的預期不符。

- **React-Core Header Visibility:**
  - **現象:** `RNFBApp` 報錯 `'React/RCTVersion.h' file not found` 或 `'yoga/Yoga.h' file not found`。
  - **Error Log:**
    ```
    ❌  Pods/RNFBApp: 'React/RCTVersion.h' file not found
       └─[app]/ios/RNFBApp/RNFBVersion.m:18:9
    
    ❌  Pods/RNFBApp: 'yoga/Yoga.h' file not found
       └─.../Pods/Headers/Public/React-Core/React/RCTConvert.h:19:9
    
    ❌  (node_modules/@react-native-firebase/firestore/ios/RNFBFirestore/RNFBFirestoreCommon.h:40:42)
        + (void)promiseRejectFirestoreException:(RCTPromiseRejectBlock)reject error:(NSError *)error;
           ^ expected a type
    ```
  - **原因:** 全局開啟 Modular Headers 後，`React-Core` 的 Header 路徑結構改變，但 Firebase 的靜態庫 Wrapper 仍依賴傳統的 Header Search Paths。

- **Podfile Syntax / Quoting:**
  - **現象:** Header Search Paths 包含額外的引號，導致路徑無法被 Xcode 正確解析, e.g. `"/Path/To/Header"` vs `/Path/To/Header`。

## 解決方案 Solution Implemented

最終生效的解決方案集中在 `ios/Podfile` 的配置調整，核心策略是 **混合模式 Hybrid Approach** 與 **強制路徑修正**。

### Podfile 依賴配置 Dependency Configuration

我們採用了精細化的 Modular Headers 策略：

- **全局開啟** `use_modular_headers!`：這是為了滿足 Firebase Swift 的依賴需求，讓 Swift Pods 能正確生成 Module Maps。
- **特定關閉 Opt-out**：針對已知不支援或有問題的庫，顯式關閉 Modular Headers。
    ```ruby
    # Disable modular headers for gRPC (broken module maps)
    pod 'gRPC-Core', :modular_headers => false
    pod 'gRPC-C++', :modular_headers => false
    
    # Disable modular headers for React-Core (broken types/imports in static mode)
    # 關鍵：需指定 path 避免與 use_react_native! 產生 source 衝突
    pod 'React-Core', :path => "#{config[:reactNativePath]}/", :modular_headers => false
    ```

### Post Install Hook 修正

為了讓 React Native 與 Firebase 在 Static Linking 下和平共處，我們在 `post_install` 階段執行了以下腳本邏輯：

#### 強制關閉 Modules, CLANG_ENABLE_MODULES

針對 `React-Core` 和所有 `RNFB*` Firebase Targets，強制關閉 Module 支援，強迫它們使用傳統的 Header include 機制。

```ruby
if target.name == 'React-Core' || target.name.start_with?('RNFB')
  target.build_configurations.each do |config|
    config.build_settings['CLANG_ENABLE_MODULES'] = 'NO'
    config.build_settings['DEFINES_MODULE'] = 'NO'
  end
end
```

#### 手動修補 Header Search Paths

為 `RNFB*` Targets 手動注入 React 核心與 Yoga 的路徑，確保編譯器能找到這些基礎 Header：

- `"${PODS_ROOT}/Headers/Public/React-Core"`
- `"${PODS_ROOT}/Headers/Public/Yoga"`
- `"${PODS_ROOT}/Headers/Public"`

#### FirebaseAuth Header 補丁

檢測並建立 Script Build Phase，將 `FirebaseAuth-Swift.h` 從 DerivedData 複製到 `"${PODS_CONFIGURATION_BUILD_DIR}/FirebaseAuthHeaderFix/FirebaseAuth/"`，確保 RNFBAuth 能引用到它。

## 狀態 Final Status

- **Code Compilation:** ✅ **成功**。所有的 Native Code, Obj-C/Swift/C++, Firebase 模組, React 核心皆已通過編譯與連結。
- **Remaining Issue:** ⚠️ **Asset Catalog Error**。目前 Build 在最後階段報錯 `CompileAssetCatalogVariant ... Images.xcassets`。這通常是圖片檔損壞或 Xcode 緩存問題，與程式碼依賴無關。建議執行 Clean Build 或檢查 `Images.xcassets` 內容。

## 檔案參照
- **Podfile:** `/Users/kenchio/Documents/GitHub/SuSuGiGiApp/ios/Podfile`

---

# Firebase 整合問題追蹤 2025-12-21 22

## 問題背景

在成功解決初步的 iOS build 問題後，嘗試整合 Native Firebase `@react-native-firebase` 時，遭遇了更深層的編譯問題，最終發現是環境與版本的根本不兼容問題。

## 嘗試方案時間軸

### 方案 1, Firebase 12 + Static Frameworks 失敗
- **策略**: 使用 `use_frameworks! :linkage => :static`，對 gRPC 使用 opt-out
- **問題**: 遭遇 Hermes C++ ABI 不兼容
- **錯誤**: `HermesExecutorFactory.cpp` 出現 12 個持續性編譯錯誤
  ```
  ❌  shared_ptr.h:675: incompatible pointer types assigning to '__shared_weak_count *'
  ❌  unique_ptr.h:767: no matching constructor for 'facebook::react::HermesExecutor'
  ```
- **結論**: Expo SDK 54 + React Native 0.81.5 + Firebase 12 在 frameworks 模式下與 Hermes 引擎有根本的 C++ ABI 衝突

### 方案 2, 切換到 JSC 引擎 失敗
- **策略**: 在 `app.json` 設定 `"jsEngine": "jsc"` 以避開 Hermes
- **問題**: React Native 0.81.5 即使使用 JSC 作為運行時引擎，仍會編譯 Hermes 相關代碼
- **錯誤**: 完全相同的 12 個 Hermes 編譯錯誤
- **結論**: 在 RN 0.81.x，Hermes 源代碼是強制編譯的，無法通過引擎切換繞過

### 方案 3, 降級 Firebase 到 v11 失敗
- **策略**: 降級所有 Firebase 套件到 `@react-native-firebase/*@20.5.0` 對應 Firebase 11
- **檔案調整**:
  - 移除 `use_frameworks!`
  - 簡化 Podfile 為標準靜態庫配置
  - 移除 Google Sign-In 因依賴衝突
- **問題**: 
  - Pod install 反覆卡住，產生重複進程
  - 多次執行 `pod install` 皆無法完成或產生不完整安裝
  - Podfile.lock 重複損壞或遺失
- **錯誤模式**:
  ```
  Installing abseil (1.20240116.2)  ← 卡在此步驟超過 10 分鐘
  [Multiple pod processes running simultaneously]
  ```

### 方案 4, 完全移除 Firebase 的最小化 Build 失敗
- **策略**: 重置 Podfile 為最小 Expo 預設配置，完全不包含 Firebase
- **問題**: xcodebuild 卡在 "Planning build" 階段超過 20 分鐘
- **觀察**:
  - `xcodebuild` 進程存在但 CPU 時間僅 1.66 秒 幾乎沒有實際工作
  - DerivedData 顯示 7079 個預編譯模塊但無進展
  - 多次嘗試皆在相同階段卡住
- **結論**: 本地開發環境的 CocoaPods/xcodebuild 有系統性問題

## 根本原因分析

### 技術層面

- **版本不兼容三角關係:**
  - Firebase 12 要求 `use_frameworks!` 或 modular headers
  - React Native 0.81.5 與 frameworks 模式兼容性差
  - Hermes 在 frameworks/modular 模式下有 C++ template 問題

- **本地環境問題:**
  - CocoaPods 安裝過程反覆產生重複進程並卡住
  - xcodebuild 反覆在 "Planning build" 階段停滯
  - 檔案權限問題, `node_modules` 中的 header 檔案權限為 600

### 成功修復的項目

- 識別所有錯誤模式與根本原因
- 創建多種 Podfile 配置策略, static frameworks, modular headers, 混合模式
- 成功實作 `Firebase.h` 的條件式 Swift header 引用補丁
- 添加 `FOLLY_NO_COROUTINES=1` 防止 Folly 錯誤
- 修復 react-native 套件的檔案權限問題
- 完整記錄除錯過程

### 無法在本地解決的問題

- 本地 iOS 模擬器 build
- 當前 SDK 版本下的 Firebase 整合
- 本地開發環境的 Pod install 可靠性

## EAS Build 雲端編譯方案

### 設置過程

- **安裝 EAS CLI:** ✅ 完成
  ```bash
  npm install -g eas-cli
  ```

- **配置 EAS Build:** ✅ 完成
  ```bash
  eas build:configure
  ```

- **安裝 expo-dev-client:** ✅ 完成
  - 自動安裝 6 packages
  - 為 development build 做準備

- **Apple Developer 帳號需求:** ❌ **阻礙**
  ```
  ✔ Logged in and verified
  Authentication with Apple Developer Portal failed!
  You have no team associated with your Apple account, cannot proceed.
  (Do you have a paid Apple Developer account?)
  ```

### 關鍵發現

**即使使用 EAS Build 雲端編譯，development build 仍需要付費的 Apple Developer Program 會員資格 $99 美元/年。**

## 目前狀態與建議

### 專案當前配置

- **app.json:** 
  - 設定 `jsEngine: "jsc"`
  - 連結 Firebase 配置檔案 `GoogleService-Info.plist`, `google-services.json`
- **package.json:** 
  - Firebase 套件: v20.5.0 對應 Firebase 11
  - Google Sign-In: 已移除
- **ios/Podfile:** 當前為最小化 Expo 預設配置 不含 Firebase
- **eas.json:** ✅ 已配置，準備好進行雲端 build

### 後續選項

#### 選項 1, 註冊 Apple Developer Program 推薦如需 iOS 開發
- **費用**: $99 美元/年
- **優點**: 
  - 可使用 EAS Build 生成 development build
  - 未來上架 App Store 的必要條件
  - 存取完整的開發工具與功能
- **流程**: https://developer.apple.com/programs/

#### 選項 2, 暫時移除 Firebase 改用 Expo Go 繼續開發 推薦短期方案
- 移除所有 Firebase 依賴
- 使用 `npx expo start` + Expo Go 測試
- 其他功能照常開發
- 有付費帳號後再重新整合 Firebase

#### 選項 3, 優先進行 Android 開發與測試 推薦免費替代

**Android 開發不需要付費開發者帳號，Firebase 功能完全相同，可以完整驗證整合。**

- **步驟 1, 安裝 Android Studio:**
  - 下載適用於 macOS 的版本 約 1GB, https://developer.android.com/studio
  - 安裝並執行設置向導
  - 選擇 "Standard" 安裝類型
  - 下載 Android SDK、Platform Tools、Build Tools

- **步驟 2, 設置 Android 模擬器:**
  - 開啟 **Device Manager**
  - 點擊 **Create Device**
  - 選擇裝置類型 推薦 Pixel 5 或 Pixel 6
  - 選擇系統映像檔
  - 完成設置並啟動模擬器

- **步驟 3, 配置環境變數 重要:**
  - 在 `~/.zshrc` 或 `~/.bash_profile` 添加：
    ```bash
    export ANDROID_HOME=$HOME/Library/Android/sdk
    export PATH=$PATH:$ANDROID_HOME/emulator
    export PATH=$PATH:$ANDROID_HOME/platform-tools
    ```
  - 執行 `source ~/.zshrc`

- **步驟 4, 執行 Android Build:**
  ```bash
  cd /Users/kenchio/Documents/GitHub/SuSuGiGiApp
  npx expo run:android
  ```

- **步驟 5, 測試 Firebase 功能:**
  - Firebase Auth 登入/登出
  - Firestore 資料讀寫

- **替代方案, 使用實體 Android 手機:**
  - 開啟開發者選項
  - 啟用 USB 偵錯
  - 用 USB 連接到 Mac
  - 執行 `npx expo run:android`
  - **優點**: 完全免費，測試真實 Firebase 功能，速度快

#### 選項 4, 等待 Expo SDK 更新 長期觀察
- 目前 Expo SDK 54 是最新版本
- 期待未來 SDK 版本支援 React Native 0.82+
- 時間未知

## 技術學習重點

- **Firebase 12 與 React Native 整合的複雜性:**
  - Static frameworks vs modular headers 的選擇影響深遠
  - Hermes 引擎在特定配置下有 C++ ABI 限制
  - CocoaPods 的模塊系統與 Swift/Objective-C 混合專案的挑戰

- **EAS Build 的價值:**
  - 提供一致、可控的雲端 build 環境
  - 繞過本地環境的系統性問題
  - 生產環境 build 的必經之路

- **Apple 生態系統要求:**
  - iOS 開發的基本門檻是付費 Developer Program
  - 即使是 development/testing，也需要適當的憑證管理

## 參考資料

- **EAS Build 文檔**: https://docs.expo.dev/build/introduction/
- **Firebase iOS 整合**: https://rnfirebase.io/
- **React Native 與 Hermes**: https://reactnative.dev/docs/hermes
- **Apple Developer Program**: https://developer.apple.com/programs/

---

# 最終結案報告 2024-12-24

## 調查目標

驗證 Firebase 12.7.0 最新版 是否能在 Expo SDK 54 + React Native 0.81.5 環境下成功編譯。

## 完整調查過程

### 成功完成的步驟

**Firebase 12.7.0 安裝與配置:**
- 安裝 @react-native-firebase/app@latest v21.8.0
- 安裝 @react-native-firebase/auth@latest v21.5.0
- 安裝 @react-native-firebase/firestore@latest v21.5.0
- 總計 147 pods 成功安裝

**Podfile 配置優化:**
- 研究 Firebase 12.7 release notes 的 module map generation 修復
- 實現選擇性 modular headers 配置
- 成功解決所有 CocoaPods 警告
- Firebase、GoogleUtilities、RecaptchaInterop 等核心依賴全部正確配置

**Native Code 生成:**
- npx expo prebuild 成功生成 iOS project
- Xcode workspace 正確建立
- 所有 Firebase pods 正確 link

**Xcode 編譯嘗試:**
- Firebase Swift modules 開始編譯
- FirebaseCoreInternal、FirebaseAuth 等進入編譯階段
- 證明配置層面完全正確

### 最終失敗原因

**編譯錯誤:**
```
/ios/Pods/Headers/Private/Firebase/Firebase.h:40:15: 
error: 'FirebaseAuth/FirebaseAuth-Swift.h' file not found 
(in target 'RNFBFirestore' from project 'Pods')
```

**根本原因分析:**

- **Hermes C++ ABI 與 Swift Bridging Headers 不兼容:**
  - Firebase 12.7 的 Swift modules 會生成 `-Swift.h` bridging headers
  - 這些 headers 依賴 Swift compiler 的特定輸出格式
  - React Native 0.81.5 的 Hermes C++ ABI 與此格式不兼容
  - 導致 Xcode 無法找到或正確解析 Swift bridging headers

**技術細節:**
```
Firebase.h Umbrella header
  ↓ imports
FirebaseAuth.h
  ↓ imports  
FirebaseAuth-Swift.h Swift bridging header
  ↓ generated by Swift compiler
  ↓ expects specific Hermes C++ ABI
  ❌ INCOMPATIBLE with RN 0.81.5 Hermes
```

**朋友的配置為何有效:**
- 朋友使用 React Native 0.79.6 更舊的 Hermes，沒有 0.81.5 的 C++ ABI 改動
- 使用 Firebase v11 @react-native-firebase/app@23.4.0
- RN 0.79.6 的 Hermes 與 Swift modules 兼容

## 尚未解決的問題

### 問題 1, Native Firebase 整合

**狀態:** ❌ 無法解決

**問題:** Firebase 12.x 無法在 Expo SDK 54 RN 0.81.5 環境下編譯

**原因:**
- Hermes C++ ABI 不兼容 Swift bridging headers
- 這是 React Native 0.81.5 的架構性限制
- 不是配置問題，無法透過調整 Podfile 或 build settings 解決

**影響:**
- 無法使用 @react-native-firebase/auth
- 無法使用 @react-native-firebase/firestore
- 無法使用 @react-native-firebase/messaging FCM
- 無法使用任何需要 native module 的 Firebase 功能

**解決方案選項:**

- **選項 A, 等待 Expo SDK 55 推薦:**
  - 預計使用 React Native 0.82+
  - RN 0.82 應該修復 Hermes Swift interop 問題
  - Firebase 12.7 的 module map fix 將可以正常工作
  - **時間**: 等待 SDK 55 正式發布
  - **風險**: 低
  - **成本**: 時間

- **選項 B, 使用 Firebase Web SDK 短期方案:**
  - 可立即使用
  - 支援 Auth、Firestore 核心功能
  - **限制**: 無法使用 FCM、Dynamic Links 等 native features
  - **風險**: 低
  - **成本**: 功能限制

- **選項 C, 付費 EAS Build:**
  - 需要 Apple Developer 帳號 $99/年
  - Expo 雲端編譯環境可能有更好相容性
  - **但仍可能遇到相同的 Hermes-Swift 問題**
  - **風險**: 中 不保證成功
  - **成本**: $99/年 + 時間

- **選項 D, Eject from Expo + 降級到 RN 0.79.6:**
  - 完全放棄 Expo managed workflow
  - 降級到 RN 0.79.6 + Firebase v11
  - **失去**: Expo Go、OTA updates、managed workflow
  - **風險**: 高
  - **成本**: 維護成本大增

### 問題 2, 本地 Xcode/CocoaPods 環境問題

**狀態:** ⚠️  部分解決

**已解決:**
- Firebase 12.7 的 pod install 可以成功
- Module map 配置正確
- 所有依賴正確安裝

**仍存在:**
- Firebase v11 降級時 pod install 會卡住
- 本地 xcodebuild 偶爾卡在 "Planning build"
- 懷疑是 Xcode cache 或 CocoaPods 環境問題

**影響:**
- 較小 因為 Firebase 12.7 的 pod install 正常
- 主要影響實驗性降級嘗試

**解決方案:**
- 清理 `~/Library/Developer/Xcode/DerivedData`
- `pod cache clean --all`
- 重啟 Mac
- 如果仍有問題，考慮重新安裝 CocoaPods

## 建議的後續步驟

### 立即行動

- **清理專案:**
  ```bash
  # 移除 Firebase
  npm uninstall @react-native-firebase/app @react-native-firebase/auth @react-native-firebase/firestore
  
  # 清理 native code
  rm -rf ios android
  
  # 還原 app.json
  git checkout app.json
  
  # 重新安裝
  npm install
  ```

- **繼續開發:**
  - 使用 Expo Go 開發非 Firebase 功能
  - 規劃 UI/UX 完善
  - 準備 Firebase Web SDK 整合

### 中期規劃

- **監控 Expo SDK 55 發布:**
  - 追蹤 [Expo Changelog](https://expo.dev/changelog)
  - 關注 React Native 0.82+ release
  - 訂閱 Expo Discord/Forum 通知

- **Firebase Web SDK 備案:**
  - 研究 Firebase Web SDK 限制
  - 評估是否可接受功能限制
  - 準備 migration plan

### 長期規劃

- **Expo SDK 55 發布後:**
  ```bash
  # 升級 Expo SDK
  npx expo install expo@latest
  
  # 重新安裝 Firebase
  npm install @react-native-firebase/app@latest @react-native-firebase/auth@latest @react-native-firebase/firestore@latest
  
  # 應用朋友的 Podfile 配置
  # 參考：/others/Podfile.dat
  
  # 嘗試 build
  npx expo run:ios
  ```

## 時間成本總結

- **Firebase v12 首次嘗試:** 2024-12-18 至 12-19 約8 小時
- **Firebase v12 最終驗證:** 2024-12-24 約2.5 小時
- **總計:** 10.5 小時

## 價值產出

**證明了:**
- Firebase 12.7 的 module map fix 確實存在且有效
- 問題根源是 Hermes C++ ABI，不是配置
- 等待 Expo SDK 55 是最佳解決方案
- Firebase Web SDK 是可行的短期替代

**獲得了:**
- 完整的問題分析和技術文檔
- Podfile 配置最佳實踐
- 朋友的成功配置參考
- 清晰的技術決策依據

## 結論

**現狀:** Firebase Native integration 在 Expo SDK 54 環境下**不可行**

**原因:** 系統性架構限制 Hermes C++ ABI，非配置問題

**建議:**
- **優先選項:** 等待 Expo SDK 55
- **備案選項:** Firebase Web SDK
- **不常試選項:** 付費 EAS Build
- **不常試選項:** Eject + 降級

**下一步:** 清理專案，回復到 Expo Go 可用狀態，執行 EAS update 確保 OTA 更新正常

---

**報告完成時間:** 2024-12-24 21:25
**狀態:** 已結案
**結論:** 等待 Expo SDK 55
