# 交易編輯器規格: TransactionEditorScreen

## 畫面目標

- **提供:** 新增, 編輯, 刪除 收入 或 支出 交易的介面
- **作為:** 建立 定期收支 排程的入口
- **處理:** 編輯由定期排程所產生交易的特殊邏輯

## UI 佈局

- **呈現方式:** Modal 形式從底部彈出
- **頂部導航列:**
    - **內部元件:**
        - **關閉按鈕**
        - **標題**
            - **內容:** 依模式顯示 新增支出, 新增收入, 編輯支出, 編輯收入
            - **備註:** 標題不可點擊
        - **定期交易按鈕**
            - **圖示:** 循環圖示
- **日期選擇區:**
    - **位置:** 導航列正下方
    - **元件:** DatePicker
    - **屬性:** 必填項
- **金額輸入區:**
    - **UI:** 大型金額輸入框, TextInput
    - **行為:** 點擊彈出原生數字鍵盤
- **核心欄位區:**
    - **UI:** 列表
    - **內部元件:**
        - **類別 (Category):**
            - **元件:** CategorySelector
            - **邏輯:** 列表依 `type` 參數 (income/expense) 過濾
            - **屬性:** 必填項
        - **帳戶 (Account):**
            - **元件:** AccountSelector
            - **邏輯:** 帳戶按 `sortOrder` 排序
            - **屬性:** 必填項
        - **備註 (Note):**
            - **UI:** 文字輸入框
- **表單提交區:**
    - **內部元件:**
        - **刪除按鈕**
            - **UI:** 紅色文字
            - **可見性:** 僅 編輯模式 顯示
        - **儲存按鈕**
            - **UI:** 主要顏色
            - **可見性:** 僅所有必填欄位有效時才可點擊

## 核心邏輯

- **定期交易按鈕邏輯:**
    - **觸發:** 點擊 定期交易按鈕
    - **檢查:** `PremiumContext.isPremiumUser`
    - **IF** False (免費版):
        - **導航:** PaywallScreen
    - **IF** True (付費版):
        - **行為:** 開啟 ScheduleModal 進行設定
- **模式判斷與預設值:**
    - **觸發:** 畫面載入
    - **檢查:** 導航參數是否傳入 `transactionId`
    - **IF** 有 `transactionId` (編輯模式):
        - **讀取:** 從 本機 DB 讀取該筆交易資料填入表單
        - **顯示:** 標題 編輯支出 / 編輯收入
        - **顯示:** 刪除按鈕
    - **IF** 無 `transactionId` (新增模式):
        - **顯示:** 標題 新增支出 / 新增收入
        - **預設值 - 日期:**
            - **檢查:** 導航參數 `defaultDate`
            - **IF** 有 `defaultDate`:
                - **行為:** 使用 `defaultDate`
            - **ELSE:**
                - **行為:** 預設為 今天
        - **預設值 - 類別/帳戶:**
            - **行為:** 預選 `sortOrder` 最高的項目
- **儲存邏輯:**
    - **觸發:** 點擊 儲存按鈕
    - **新增模式:**
        - **IF** 未設定重複規則:
            - **行為:** 於 本機 DB 建立新 `Transaction` 記錄
            - **欄位:** 必須設定 `updatedOn`
        - **IF** 設定重複規則 (付費功能):
            - **觸發:** 執行 建立邏輯
            - **定義:** 參見 `no6_5_recurring_transaction_spec`
    - **編輯模式:**
        - **檢查:** 該筆交易 `scheduleInstanceDate` 是否有值
        - **IF** `scheduleInstanceDate` 為 null (普通交易):
            - **行為:** 更新 本機 DB 該筆 `Transaction` 記錄
            - **欄位:** 必須更新 `updatedOn`
        - **IF** `scheduleInstanceDate` 有值 (定期交易):
            - **觸發:** 執行 編輯/刪除邏輯
            - **定義:** 參見 `no6_5_recurring_transaction_spec`
    - **成功:**
        - **導航:** 關閉畫面, 返回前一頁
- **刪除邏輯:**
    - **條件:** 僅 編輯模式 可用
    - **觸發:** 點擊 刪除按鈕
    - **檢查:** 該筆交易 `scheduleInstanceDate` 是否有值
    - **IF** `scheduleInstanceDate` 為 null (普通交易):
        - **行為:** 軟刪除 本機 DB 該筆 `Transaction`
        - **欄位:** 必須設定 `deletedOn` 並更新 `updatedOn`
    - **IF** `scheduleInstanceDate` 有值 (定期交易):
        - **觸發:** 執行 編輯/刪除邏輯
        - **定義:** 參見 `no6_5_recurring_transaction_spec`
    - **成功:**
        - **導航:** 關閉畫面, 返回前一頁

## 狀態管理

- **來自導航:**
    - `type`: 'expense' | 'income'
- **本地狀態:**
    - `amountCents`
    - `categoryId`
    - `accountId`
    - `transactionDate`
    - `note`
    - `schedule`

## 導航

- **進入:**
    - **來源:** HomeScreen
    - **必要參數:**
        - `type`: 'income' | 'expense'
    - **可選參數:**
        - `transactionId`
        - `defaultDate`
- **退出:**
    - **觸發:** 點擊 關閉按鈕, 或 儲存/刪除 成功
    - **行為:** `navigation.goBack()`