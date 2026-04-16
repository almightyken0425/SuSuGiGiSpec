# 轉帳核心邏輯: TransferLogic

## createTransfer 建立轉帳

- 建立轉帳紀錄，跨幣別時 Append-Only 補錄隱含匯率
- **輸入:**
  - 轉帳資料
- **寫入 Transfer:**
  - **執行:**
    - 新增一筆記錄至 `Transfers` 表
- **匯率連動 Append-Only:**
  - **條件:**
    - 跨幣別轉帳且有隱含匯率
  - **執行:**
    - 新增一筆記錄至 `CurrencyRates` 表

## updateTransfer 更新轉帳

- **輸入:**
  - 轉帳資料
- **更新 Transfer:**
  - **執行:**
    - 更新 `Transfers` 表中的記錄
- **匯率連動 Append-Only:**
  - **條件:**
    - 跨幣別且隱含匯率變動或交易日期變動
  - **執行:**
    - 新增一筆記錄至 `CurrencyRates` 表

## deleteTransfer 刪除轉帳

- **輸入:**
  - 轉帳識別碼
- **軟刪除 Transfer:**
  - **執行:**
    - 更新 `Transfers` 表
- **匯率連動:**
  - **行為:**
    - 不刪除任何已產生的匯率記錄