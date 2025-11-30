# 轉帳編輯器規格: TransferEditorScreen

## 畫面目標

- **提供:** 新增, 編輯, 刪除 轉帳 記錄的介面
- **支援:** 同幣別轉帳 與 跨幣別轉帳
- **作為:** 建立 定期轉帳 排程的入口
- **處理:** 編輯由定期排程所產生轉帳的特殊邏輯

```text
+--------------------------------+
| Cancel    Transfer      Submit |
+--------------------------------+
|  Date: Oct 25, 2024 (Full)     |
+--------------------------------+
| From: [Account Selector]       |
| To:   [Account Selector]       |
| Note: [Note Input]             |
+--------------------------------+
| Amount From: [ $ Input ] [Recur]|
| (Rate & Arrow if Cross-Currency)|
| Amount To:   [ $ Input ]       |
|                                |
|           [Delete]             |
+--------------------------------+
```

## UI 佈局

- **呈現方式:** Modal 形式從底部彈出
- **頂部導航列 Header:**
    - **內部元件:**
        - **左側:** 關閉按鈕 Cancel
        - **中間:** 標題 轉帳
        - **右側:** 完成按鈕 Submit
            - **可見性:** 所有必填欄位有效 且 轉出!=轉入
- **日期選擇區 Top of Body:**
    - **位置:** 緊接於 Header 下方，金額輸入框之上
    - **結構 - 預設折疊狀態:**
        - **UI:** 顯示格式化日期文字的觸發區域
        - **格式:** MD
        - **禁止:** 不顯示年份與時分秒
    - **行為 - 互動:**
        - **觸發:** 點擊預設狀態 UI
        - **行為:** 展開 Modal 或日曆視圖
    - **結構 - 展開狀態:**
        - **內部元件:**
            - **日曆:**
                - **行為:** 允許使用者選擇 年/月/日
                - **綁定:** 寫入 `transactionDate`
            - **時間選擇器:**
                - **UI:** 滾輪或輸入框
                - **行為:** 允許使用者選擇 時/分/秒
                - **精確度:** 支援至秒 (S)
    - **屬性:** 必填項
- **帳戶選擇區:**
    - **內部元件:**
        - **轉出帳戶:**
            - **元件:** AccountSelector
            - **邏輯:** 列表按 `sortOrder` 排序
            - **屬性:** 必填項
        - **轉入帳戶:**
            - **元件:** AccountSelector
            - **邏輯:** 列表按 `sortOrder` 排序
            - **屬性:** 必填項
    - **防呆邏輯:**
        - **條件:** 轉出帳戶 等於 轉入帳戶
        - **UI:** 顯示錯誤狀態
- **備註區:**
    - **UI:** 文字輸入框
- **金額輸入區 Main Body:**
    - **UI:** 上下垂直排列
    - **內部元件:**
        - **轉出金額 Amount From:**
            - **UI:** 橫向排列, 大型金額輸入框
            - **屬性:** 必填項
            - **附屬元件:**
                - **定期交易按鈕:** 位於轉出金額右側, 點擊開啟 ScheduleModal
        - **匯率與箭頭:**
            - **可見性:** 僅 跨幣別轉帳 時顯示
            - **UI:** 向下箭頭, 顯示即時計算的隱含匯率
        - **轉入金額 Amount To:**
            - **UI:** 大型金額輸入框, 彈出原生數字鍵盤
            - **邏輯:**
                - **同幣別轉帳:**
                    - **可見性:** 不顯示
                    - **儲存:** amountToCents = amountFromCents
                - **跨幣別轉帳:**
                    - **可見性:** 顯示並可編輯
- **底部區域 Footer:**
    - **內部元件:**
        - **刪除按鈕**
            - **UI:** 紅色文字或按鈕, 位於畫面最底部
            - **可見性:** 僅 編輯模式 顯示

---

## 核心邏輯

- **定期交易按鈕邏輯:**
    - **觸發:** 點擊 定期交易按鈕
    - **檢查:** `PremiumContext.isPremiumUser`
    - **IF** False 免費版:
        - **導航:** PaywallScreen
    - **IF** True 付費版:
        - **行為:** 開啟 ScheduleModal 進行設定
- **模式判斷與預設值:**
    - **觸發:** 畫面載入
    - **檢查:** 導航參數 `transferId`
    - **IF** 有 `transferId` 編輯模式:
        - **讀取:** 從 本機 DB 讀取轉帳資料填入表單
        - **顯示:** 刪除按鈕
    - **IF** 無 `transferId` 新增模式:
        - **預設值 - 日期:**
            - **檢查:** 導航參數 `defaultDate`
            - **IF** 有 `defaultDate`:
                - **行為:** 使用 `defaultDate`
            - **ELSE:**
                - **行為:** 預設為 裝置目前時間 (含時分秒)
        - **預設值 - 帳戶:**
            - **轉出帳戶:** 預選 `sortOrder` 最高的項目
            - **轉入帳戶:** 預選 `sortOrder` 第二高的項目
            - **IF** 帳戶 < 2 個:
                - **轉入帳戶:** 留空
                - **儲存按鈕:** 禁用
- **儲存邏輯:**
    - **觸發:** 點擊 儲存按鈕
    - **新增模式:**
        - **跨幣別匯率記錄:**
            - **條件:** 轉出與轉入帳戶的幣別不同
            - **檢查:** `PremiumContext.isPremiumUser`
            - **IF** False 免費版:
                - **導航:** PaywallScreen
            - **IF** True 付費版:
                - **計算:** 隱含匯率 rateCents
                - **儲存:** 於 本機 DB 批次新增 `CurrencyRates` 記錄
                - **欄位:** 必須設定 `updatedOn`
                - **備註:** rateDate 設為該筆轉帳的 transactionDate
        - **IF** 未設定重複規則:
            - **行為:** 於 本機 DB 建立新 `Transfer` 記錄
            - **欄位:** 必須設定 `updatedOn`
        - **IF** 設定重複規則:
            - **觸發:** 執行 建立邏輯
    - **編輯模式:**
        - **檢查:** 該筆轉帳 `scheduleInstanceDate` 是否有值
        - **IF** `scheduleInstanceDate` 為 null 一般轉帳:
            - **行為:** 更新 本機 DB 該筆 `Transfer` 記錄
            - **欄位:** 必須更新 `updatedOn`
        - **IF** `scheduleInstanceDate` 有值 定期轉帳:
            - **觸發:** 執行 編輯/刪除邏輯
    - **成功:**
        - **導航:** 關閉畫面, 返回前一頁
- **刪除邏輯:**
    - **條件:** 僅 編輯模式 可用
    - **觸發:** 點擊 刪除按鈕
    - **檢查:** 該筆轉帳 `scheduleInstanceDate` 是否有值
    - **IF** `scheduleInstanceDate` 為 null 一般轉帳:
        - **行為:** 軟刪除 本機 DB 該筆 `Transfer`
        - **欄位:** 必須設定 `deletedOn` 並更新 `updatedOn`
    - **IF** `scheduleInstanceDate` 有值 定期轉帳:
        - **觸發:** 執行 編輯/刪除邏輯
    - **成功:**
        - **導航:** 關閉畫面, 返回前一頁

---

## 狀態管理

- **本地狀態:**
    - `accountFromId`
    - `accountToId`
    - `amountFromCents`
    - `amountToCents`
    - `transactionDate`
    - `note`
    - `schedule`

---

## 導航

- **進入:**
    - **來源:** HomeScreen
    - **可選參數:**
        - `transferId`
        - `defaultDate`
- **退出:**
    - **觸發:** 點擊 關閉按鈕, 或 儲存/刪除 成功
    - **行為:** `navigation.goBack()`