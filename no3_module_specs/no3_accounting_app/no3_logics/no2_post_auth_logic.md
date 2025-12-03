# 登入認證後邏輯

## 觸發時機

- **觸發:** 認證成功時，由 `LoginScreen` 觸發

## 權限檢查

- **檢查:** 呼叫 `PremiumLogic.refreshPremiumStatus()` 更新本地權限狀態

## 舊用戶邏輯 Premium

- **條件:** `PremiumLogic.checkPremiumStatus()` 為 True
- **讀取 User Profile:**
    - **行為:** 嘗試讀取 Firestore `users/{uid}`
- **IF 讀取成功:**
    - **解析:** Firestore 回傳的 `preferences` (language, currency, timezone)
    - **覆蓋寫入:** 本機 DB `Settings` 表
        - `language` = `preferences.language`
        - `baseCurrencyId` = `preferences.currency` (需轉換 ISO code to ID)
        - `timeZone` = `preferences.timezone`
        - `theme` = `preferences.theme`
        - `updatedOn` = Current Timestamp
    - **後續:** 觸發同步與定期交易檢查

## 新用戶或訪客轉正邏輯

- **條件:** 讀取失敗、文件不存在 或 `PremiumLogic.checkPremiumStatus()` 為 False
- **執行:** 初始化流程
- **決定預設值:**
    - **主要幣別:** 嘗試從裝置 Locale 取得，若無則預設 TWD (需轉換為 ISO Code)
    - **語系:** 嘗試從裝置 Locale 取得，若無則預設系統語言
    - **時區:** 讀取裝置時區
    - **主題:** 預設 system
- **寫入本機 App Onboarding:**
    - **建立:** 本機 DB `Settings` 表資料 (需將 ISO Code 轉為 Currency ID)
    - **建立預設資料:**
        - 帳戶: 現金 (使用主要幣別)
        - 類別: 食衣住行標準類別
- **寫入雲端 User Management Onboarding:**
    - **條件:** 僅在 `PremiumLogic.checkPremiumStatus()` 為 True 時執行
    - **建立:** Firestore `users/{uid}` 文件
    - **內容:**
        - `uid`, `email`, `provider`
        - `preferences`: { language, currency, timezone, theme } (儲存 ISO Code)
        - `createdAt`: Server Timestamp
- **備註:** 不執行 Batch Sync，因無資料需下載