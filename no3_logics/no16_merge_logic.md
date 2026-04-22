# 合併邏輯: MergeLogic

## mergeAccounts 合併帳戶

- **輸入:**
  - 來源帳戶識別碼
  - 目標帳戶識別碼
- **前置檢查:**
  - **IF** 來源與目標幣別不同:
    - **回傳:** 錯誤，中止流程
- **轉移 Transaction:**
  - **執行:**
    - 更新屬於來源的 `Transactions` 表記錄，將所屬帳戶改為目標
- **轉移 Transfer:**
  - **執行:**
    - 更新以來源為轉出方的 `Transfers` 表記錄，將轉出方改為目標
    - 更新以來源為轉入方的 `Transfers` 表記錄，將轉入方改為目標
- **去除冗餘 Transfer:**
  - **IF** 轉移後某筆 Transfer 的轉出方與轉入方相同:
    - **執行:**
      - 軟刪除該筆 `Transfers` 表記錄
- **軟刪除 Account:**
  - **執行:**
    - 更新來源在 `Accounts` 表的記錄

## mergeCategories 合併分類

- **輸入:**
  - 來源分類識別碼
  - 目標分類識別碼
- **轉移 Transaction:**
  - **執行:**
    - 更新屬於來源的 `Transactions` 表記錄，將所屬分類改為目標
- **軟刪除 Category:**
  - **執行:**
    - 更新來源在 `Categories` 表的記錄
