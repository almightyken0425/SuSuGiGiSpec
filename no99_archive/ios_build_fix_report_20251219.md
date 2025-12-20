# iOS Build Troubleshooting Report - 2025-12-19

## 背景 (Context)
在整合 Native Firebase (`@react-native-firebase`) 到 Expo 專案 (Static Linking 模式) 時，遭遇了嚴重的 iOS 編譯錯誤。主要涉及 CocoaPods 的 Header Search Paths、Module Maps 以及靜態/動態庫的相容性衝突。這份報告記錄了問題的根源與最終的解決方案，以備日後維護參考。

## 遭遇問題 (Problems Encountered)

在此次除錯過程中，我們依序解決了以下數個核心錯誤：

1.  **Duplicate Tasks Error:** 
    - **現象:** Build 失敗，顯示多個 Target (`RNFBApp`, `RNFBAuth` 等) 試圖同時執行同一個 Copy Script。
    - **Error Log:**
      ```
      Run script build phase 'Copy FirebaseAuth Swift Header' will be run during every build because it does not specify any outputs...
      (in target 'RNFBAuth' from project 'Pods')
      (in target 'RNFBFirestore' from project 'Pods')
      (in target 'RNFBApp' from project 'Pods')
      ```
    - **原因:** `Podfile` 中的 `post_install` hook 對每個 Target 都重複添加了相同的 Script Build Phase。

2.  **Missing Headers (FirebaseAuth & FirebaseCore):** 
    - **現象:** `'FirebaseAuth/FirebaseAuth-Swift.h' file not found` 或 `'Firebase/Firebase.h' file not found`。
    - **Error Log:**
      ```
      ❌  Pods/RNFBApp: 'Firebase/Firebase.h' file not found
         └─[app]/ios/RNFBApp/RNFBAppModule.m:18:9
      ❌  Pods/RNFBApp: 'FirebaseCore/FirebaseCore.h' file not found
      ```
    - **原因:** 在 Static Library 模式下，CocoaPods 默認不會將 Swift Compatibility Header 暴露到標準路徑。

3.  **Module Map Conflict (gRPC):** 
    - **現象:** 開啟 `use_modular_headers!` 後，出現 `module 'gRPC' not found` 或重新定義錯誤。
    - **Error Log (Partial):**
      ```
      [!] The following Swift pods cannot yet be integrated as static libraries:
      The Swift pod `FirebaseAuth` depends upon ... `RecaptchaInterop`, which do not define modules.
      ```
    - **原因:** gRPC 系列套件 (`gRPC-Core`, `gRPC-C++`) 的 module map 定義與 React Native 或 Firebase 的預期不符。

4.  **React-Core Header Visibility:** 
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

5.  **Podfile Syntax / Quoting:**
    - **現象:** Header Search Paths 包含額外的引號，導致路徑無法被 Xcode 正確解析 (e.g., `"/Path/To/Header"` vs `/Path/To/Header`)。

## 解決方案 (Solution Implemented)

最終生效的解決方案集中在 `ios/Podfile` 的配置調整，核心策略是 **"混合模式" (Hybrid Approach)** 與 **"強制路徑修正"**。

### 1. Podfile 依賴配置 (Dependency Configuration)

我們採用了精細化的 Modular Headers 策略：

- **全局開啟** `use_modular_headers!`：這是為了滿足 Firebase (Swift) 的依賴需求，讓 Swift Pods 能正確生成 Module Maps。
- **特定關閉 (Opt-out)**：針對已知不支援或有問題的庫，顯式關閉 Modular Headers。
    ```ruby
    # Disable modular headers for gRPC (broken module maps)
    pod 'gRPC-Core', :modular_headers => false
    pod 'gRPC-C++', :modular_headers => false
    
    # Disable modular headers for React-Core (broken types/imports in static mode)
    # 關鍵：需指定 path 避免與 use_react_native! 產生 source 衝突
    pod 'React-Core', :path => "#{config[:reactNativePath]}/", :modular_headers => false
    ```

### 2. Post Install Hook 修正

為了讓 React Native 與 Firebase 在 Static Linking 下和平共處，我們在 `post_install` 階段執行了以下腳本邏輯：

#### A. 強制關閉 Modules (CLANG_ENABLE_MODULES)
針對 `React-Core` 和所有 `RNFB*` (Firebase) Targets，強制關閉 Module 支援，強迫它們使用傳統的 Header include 機制。

```ruby
if target.name == 'React-Core' || target.name.start_with?('RNFB')
  target.build_configurations.each do |config|
    config.build_settings['CLANG_ENABLE_MODULES'] = 'NO'
    config.build_settings['DEFINES_MODULE'] = 'NO'
  end
end
```

#### B. 手動修補 Header Search Paths
為 `RNFB*` Targets 手動注入 React 核心與 Yoga 的路徑，確保編譯器能找到這些基礎 Header：

- `"${PODS_ROOT}/Headers/Public/React-Core"`
- `"${PODS_ROOT}/Headers/Public/Yoga"`
- `"${PODS_ROOT}/Headers/Public"`

#### C. FirebaseAuth Header 補丁
檢測並建立 Script Build Phase，將 `FirebaseAuth-Swift.h` 從 DerivedData 複製到 `"${PODS_CONFIGURATION_BUILD_DIR}/FirebaseAuthHeaderFix/FirebaseAuth/"`，確保 RNFBAuth 能引用到它。

## 最終狀態 (Final Status)

- **Code Compilation:** ✅ **成功**。所有的 Native Code (Obj-C/Swift/C++)、Firebase 模組、React 核心皆已通過編譯與連結。
- **Remaining Issue:** ⚠️ **Asset Catalog Error**。目前 Build 在最後階段報錯 `CompileAssetCatalogVariant ... Images.xcassets`。這通常是圖片檔損壞或 Xcode 緩存問題，與程式碼依賴無關。建議執行 Clean Build 或檢查 `Images.xcassets` 內容。

## 檔案參照
- **Podfile:** `/Users/kenchio/Documents/GitHub/SuSuGiGiApp/ios/Podfile`
