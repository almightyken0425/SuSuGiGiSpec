# 阻礙問題解決報告：Firestore 編譯錯誤 (已解決)

**日期:** 2026-01-08
**狀態:** ✅ Build Success (With Firestore)

## 1. 問題回顧

在 React Native 0.79.6 專案中，整合 Firebase Firestore 時，曾遭遇 `leveldb-library` 的 `non-modular-include` 錯誤。

## 2. 最終成功配置

經過用戶堅持重試與重新配置，我們確認了以下組合可以成功編譯：

1.  **版本一致性:**
    - `@react-native-firebase/app`: `21.14.0`
    - `@react-native-firebase/auth`: `21.14.0`
    - `@react-native-firebase/firestore`: `21.14.0` (務必鎖定版本，避免安裝到 v23.x 導致 peer dependency 衝突)
2.  **Podfile 關鍵設定:**
    - 使用 `pre_install` hook 將 Firebase pods 設定為 static frameworks。
    - 加入 `config.build_settings['CLANG_ALLOW_NON_MODULAR_INCLUDES_IN_FRAMEWORK_MODULES'] = 'YES'`。
3.  **Clean Build:**
    - 徹底清除 `ios/build`, `ios/Pods`, `Podfile.lock` 並重新安裝。

## 3. 結果

- ✅ **iOS Build 成功:** 包含 Firestore 的完整 App 成功編譯。
- ✅ **App 啟動成功:** 模擬器順利進入登入畫面。

## 4. 驗證行動

請執行以下測試驗證由 "Clean Install" 帶來的影響：
1.  **Google Sign-In:** 測試登入流程。
2.  **Firestore:** (若有實作) 測試資料讀取/寫入。
