# 當前阻礙問題報告：Firestore 編譯錯誤

**日期:** 2026-01-08
**狀態:** ❌ Build Failed (Blocker)

## 1. 問題摘要

在 React Native 0.79.6 專案中，當整合 Firebase Firestore 時，iOS 專案無法通過編譯。錯誤發生在 Firestore 的底層 C++ 依賴 `leveldb-library`。

即使 Firebase Auth 和其他功能配置正確，只要包含 `FirebaseFirestore`，`xcodebuild` 就會失敗 (Exit code 65)。

---

## 2. 環境資訊

- **React Native:** `0.79.6`
- **React Native Firebase:** `21.14.0`
- **Firebase iOS SDK:** `11.11.0`
- **Podfile 設定:** `use_frameworks! :linkage => :static`
- **Xcode:** 最新版
- **模擬器:** iPhone 16 Pro (iOS 18.3)

---

## 3. 具體錯誤訊息

**錯誤類型:** `non-modular-include-in-framework-module`

**發生位置:** `leveldb-library` (Google 的 Key-Value 存儲庫，Firestore 依賴項)

**日誌片段:**
```text
leveldb-library/util/hash.cc
error: include of non-modular header inside framework module 'leveldb_library'

leveldb-library/table/format.cc
error: include of non-modular header inside framework module 'leveldb_library'

...
error: Failed to build ios project. "xcodebuild" exited with error code '65'.
```

**技術原因:**
React Native 0.79 強制或預設使用 `use_frameworks!` (Static Frameworks)。這啟用了 Clang 編譯器的嚴格模組驗證。`leveldb-library` 是一個較舊的 C++ 庫，其標頭檔 (Headers) 的引用方式不符合現代 iOS Framework 的模組化規範 (Modular Header specs)。

---

## 4. 已嘗試的解決方案 (皆失敗)

### 嘗試 1: 降級 Firebase 版本
- **測試:** Firebase v23.x (iOS 12.x), v21.x (iOS 11.x), v20.x (iOS 10.x)
- **結果:** 所有版本均依賴 `leveldb-library`，錯誤完全相同。

### 嘗試 2: 修改 Podfile 編譯旗標
- **操作:** 在 `post_install` hook 中為所有 targets 加入設定：
  ```ruby
  config.build_settings['CLANG_ALLOW_NON_MODULAR_INCLUDES_IN_FRAMEWORK_MODULES'] = 'YES'
  ```
- **結果:** 無效。Clang 在編譯 Framework 內部的 C++ 檔案時仍然報錯。

### 嘗試 3: 靜態 Framework 配置
- **操作:** 參照成功案例，將 Firebase 相關 Pods 明確標記為靜態 Framework 並開啟 `modular_headers => true`。
- **結果:** Pod install 成功，但編譯階段 LevelDB 依然失敗。

---

## 5. 當前結論與選項

**根因:** React Native 0.79.6 的 iOS 建置環境與 `leveldb-library` 的代碼結構存在根本性的兼容性衝突。

**可行選項:**

1.  **暫時移除 Firestore (推薦)**
    - **操作:** `npm uninstall @react-native-firebase/firestore`
    - **優點:** 立即解除 Block，可驗證 Auth 與 Google Sign-In 功能。
    - **缺點:** 暫時無法使用資料庫功能。

2.  **降級 React Native 版本**
    - **操作:** 降級至 0.76.x 或更早版本。
    - **優點:** 舊版 RN 對 Static Framework 要求較寬鬆，可能避開此問題。
    - **缺點:** 工程浩大，需重構專案。

3.  **等待或尋找 Patch**
    - **操作:** 尋找針對 `leveldb-library` 的 patch-package 或是等待官方修復。
    - **現狀:** 當前無現成可用的 Patch。
