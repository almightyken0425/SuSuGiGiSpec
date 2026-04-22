# 帳戶核心邏輯: AccountLogic

## createAccount 建立帳戶

- **輸入:**
  - 帳戶資料
- **寫入 Account:**
  - **執行:**
    - 新增一筆記錄至 `Accounts` 表
- **IF** 幣別非基礎幣別:
  - **呼叫:**
    - `CurrencyConversionLogic.createInitialCurrencyRate`

## updateAccount 更新帳戶

- **輸入:**
  - 帳戶資料
- **更新 Account:**
  - **執行:**
    - 更新 `Accounts` 表中的記錄

## deleteAccount 刪除帳戶

- **輸入:**
  - 帳戶識別碼
- **軟刪除 Account:**
  - **執行:**
    - 更新 `Accounts` 表
- **串聯軟刪除 Transaction:**
  - **執行:**
    - 更新該帳戶所屬的 `Transactions` 表記錄
- **串聯軟刪除 Transfer:**
  - **執行:**
    - 更新該帳戶作為轉出方或轉入方的 `Transfers` 表記錄

## reorderAccounts 重排帳戶

- **輸入:**
  - 有序的帳戶識別碼清單
- **更新 Account:**
  - **執行:**
    - 批次更新 `Accounts` 表的排序欄位
