# 交易核心邏輯: TransactionLogic

## createTransaction 建立交易

- **輸入:**
  - 交易資料
- **寫入 Transaction:**
  - **執行:**
    - 新增一筆記錄至 `Transactions` 表

## updateTransaction 更新交易

- **輸入:**
  - 交易資料
- **更新 Transaction:**
  - **執行:**
    - 更新 `Transactions` 表中的記錄

## deleteTransaction 刪除交易

- **輸入:**
  - 交易識別碼
- **軟刪除 Transaction:**
  - **執行:**
    - 更新 `Transactions` 表
