# 定期交易規格: RecurringTransactions

## 建立邏輯

- **觸發:**
    - 於 `TransactionEditorScreen` 或 `TransferEditorScreen`
    - 使用者設定重複規則並儲存
- **行為:**
    - 於 `Schedules` 表建立一筆新記錄
    - 立即為 `startOn` 日期產生第一筆交易實例
        - **資料:** `Transaction` 或 `Transfer`
        - **欄位:** 包含 `scheduleId` 及 `scheduleInstanceDate`

---

## 補產生邏輯 App 啟動時

- **讀取:** 本地儲存 `lastRecurringCheckDate`
- **計算:** 基於使用者主要時區的當前日期 `currentDateInUserTZ`
- **判斷:**
    - **IF** `currentDateInUserTZ` > `lastRecurringCheckDate`:
        - **執行:** 遍歷所有 `deletedOn` 為 null 的 `Schedules`
        - **計算:** 找出從 `lastRecurringCheckDate` 之後到 `currentDateInUserTZ` 當日為止, 所有應產生的日期 `instanceDate`
        - **檢查重複:** 逐筆檢查
            - **查詢:** `Transactions` / `Transfers` 表
            - **條件:** `scheduleId` 與 `scheduleInstanceDate` 組合匹配 `instanceDate`, 無論 `deletedOn` 狀態
        - **產生交易:**
            - **IF** 檢查不存在:
                - **行為:** 使用 `Schedule` 模板創建新記錄
                - **欄位:** `scheduleId`, `scheduleInstanceDate`
                - **備註:** `transactionDate` 欄位值設為 `instanceDate`
            - **IF** 檢查已存在:
                - **行為:** 跳過, 不執行任何操作
        - **更新:** `lastRecurringCheckDate` = `currentDateInUserTZ`

---

## 編輯/刪除邏輯

- **觸發:** 使用者於 `TransactionEditorScreen` / `TransferEditorScreen` 編輯或刪除一筆由定期交易產生的記錄
- **條件:** 該記錄的 `scheduleInstanceDate` 非 null
- **UI:** 顯示選項
    - **僅此一筆:**
        - **編輯:**
            - **行為:** 直接修改該筆 `Transaction` / `Transfer`
        - **刪除:**
            - **行為:** 軟刪除該筆 `Transaction` / `Transfer`
    - **此筆及未來所有:**
        - **編輯:**
            - **行為:**
                - 將原 `Schedule` 的 `endOn` 設為此交易日期的前一週期
                - 根據新內容創建一個新 `Schedule`
                - 不修改任何歷史記錄
        - **刪除:**
            - **行為:**
                - 將原 `Schedule` 的 `endOn` 設為此交易日期的前一週期
                - 不修改任何歷史記錄