# 登入後初始化流程: PostAuthLogic

## handlePostAuth 處理登入後初始化

- 認證成功後，刷新 Premium 狀態並依用戶資料來源分派初始化路徑
- **執行:**
  - 向 IAP 服務查詢最新購買憑證，更新本地 Premium 到期狀態
  - 查詢本地 Premium 權限狀態
  - **IF** Premium 有效:
    - 嘗試讀取 Firestore `users/{uid}` 文件
    - **IF** 讀取成功且文件存在:
      - 呼叫 syncSettingsFromCloud
    - **ELSE** 文件不存在或讀取失敗:
      - 呼叫 initializeNewUser
  - **ELSE** Premium 無效:
    - 呼叫 initializeNewUser

---

## syncSettingsFromCloud 從雲端同步設定

- 以 Last Write Wins 策略將雲端偏好設定同步至本機 Settings 表
- **輸入:**
  - Firestore `users/{uid}` 文件資料
- **執行:**
  - 取得 preferences 的 language、currency、timezone、theme，及 updatedAt 作為遠端時間
  - 讀取本機 Settings 表的 updatedOn 作為本機時間
  - **IF** 遠端時間大於本機時間，或本地無資料:
    - **寫入 Settings:**
      - **執行:**
        - 將雲端偏好覆寫至本機 Settings 表
      - **欄位:**
        - `language`
        - `baseCurrencyId`
        - `timeZone`
        - `theme`
        - `updatedOn`
  - **ELSE** 本機時間大於遠端時間:
    - 不覆寫本機設定，不執行任何動作
- **觸發:**
  - 批次同步與定期交易檢查

---

## initializeNewUser 初始化新用戶

- 依裝置 Locale 決定預設值，建立本機資料，並視 Premium 狀態決定是否同步至 Firestore
- **執行:**
  - **決定預設值:**
    - **執行:**
      - 主要幣別:
        - 從裝置 Locale 取得
        - 若無則預設 TWD，並轉換為 Currency ID
      - 語系:
        - 從裝置 Locale 取得
        - 若無則預設系統語言
      - 時區:
        - 讀取裝置時區
      - 主題:
        - 預設 Default
  - **建立本機資料:**
    - **執行:**
      - 新增記錄至 Users 表及 Settings 表
      - 產生預設收支分類及現金帳戶
    - **欄位:**
      - `baseCurrencyId`: 依主要幣別決定
      - `language`: 依語系決定
      - `timeZone`: 依時區決定
      - `theme`: Default
  - **建立雲端用戶文件:**
    - **條件:**
      - Premium 有效
    - **執行:**
      - 在 Firestore 建立 `users/{uid}` 文件
    - **欄位:**
      - `uid`, `email`, `provider`
      - `preferences`
      - `createdAt`
