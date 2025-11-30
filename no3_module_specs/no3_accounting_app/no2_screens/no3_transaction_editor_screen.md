# 交易編輯器規格: TransactionEditorScreen

## 畫面目標

- **提供:** 新增, 編輯, 刪除 收入 或 支出 交易的介面
- **作為:** 建立 定期收支 排程的入口
- **處理:** 編輯由定期排程所產生交易的特殊邏輯

```text
+--------------------------------+
| Cancel      Title       Submit |
+--------------------------------+
|      Date: MM/DD (Day)         |
+--------------------------------+
| [ $ Amount Input             ] |
|                                |
| [Category Selector]            |
| [Account Selector]             |
| [Note Input]                   |
|                                |
|                                |
|           [Delete]             |
+--------------------------------+
```

## UI 佈局

- **呈現方式:** Modal 形式從底部彈出
- **頂部導航列 Header:**
    - **內部元件:**
        - **左側:** 關閉按鈕 Cancel
        - **中間:** 標題 依模式顯示 支出/收入
        - **右側:** 完成按鈕 Submit
            - **可見性:** 僅所有必填欄位有效時才可點擊
- **日期選擇區 Top of Body:**
    - **位置:** 緊接於 Header 下方，金額輸入框之上
    - **結構 - 預設折疊狀態:**
        - **UI:** 顯示格式化日期文字的觸發區域
        - **格式:** 月/日 ,星期幾
        - **禁止:** 不顯示年份
        - **禁止:** 不顯示時分
    - **行為 - 互動:**
        - **觸發:** 點擊預設狀態 UI
        - **行為:** 展開 Modal 或日曆視圖
    - **結構 - 展開狀態:**
        - **內部元件:**
            - **日曆:**
                - **行為:** 允許使用者選擇 年/月/日
            - **時間選擇觸發器:**
                - **UI:** 低調的按鈕或連結
    - **行為 - 時間選擇:**
        - **觸發:** 點擊 時間選擇觸發器
        - **行為:** 展開 時/分 選擇器
        - **禁止:** 不提供秒數選擇
    - **行為 - 儲存:**
        - **IF:** 使用者未曾手動調整時分
            - **行為:** 儲存時, 時間戳記預設為當前裝置時間
        - **IF:** 使用者手動調整過時分
            - **行為:** 儲存時, 使用使用者選擇的精確時分
    - **屬性:** 必填項
- **金額輸入區 Main Body:**
    - **UI:** 橫向排列
    - **內部元件:**
        - **金額輸入框:** 大型 TextInput, 點擊彈出原生數字鍵盤
        - **定期交易按鈕:**
            - **位置:** 位於金額輸入框右側
            - **圖示:** 循環圖示
            - **行為:** 開啟定期交易設定 Modal
- **核心欄位區:**
    - **UI:** 列表
    - **內部元件:**
        - **類別 Category:**
            - **元件:** CategorySelector
            - **邏輯:** 列表依 `type` 參數 income/expense 過濾
            - **屬性:** 必填項
        - **帳戶 Account:**
            - **元件:** AccountSelector
            - **邏輯:** 帳戶按 `sortOrder` 排序
            - **屬性:** 必填項
        - **備註 Note:**
            - **UI:** 文字輸入框
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
    - **檢查:** 導航參數是否傳入 `transactionId`
    - **IF** 有 `transactionId` 編輯模式:
        - **讀取:** 從 本機 DB 讀取該筆交易資料填入表單
        - **顯示:** 標題 編輯支出 / 編輯收入
        - **顯示:** 刪除按鈕
    - **IF** 無 `transactionId` 新增模式:
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
        - **IF** 設定重複規則 付費功能:
            - **觸發:** 執行 建立邏輯
            - **定義:** 參見 `no6_5_recurring_transaction_spec`
    - **編輯模式:**
        - **檢查:** 該筆交易 `scheduleInstanceDate` 是否有值
        - **IF** `scheduleInstanceDate` 為 null 普通交易:
            - **行為:** 更新 本機 DB 該筆 `Transaction` 記錄
            - **欄位:** 必須更新 `updatedOn`
        - **IF** `scheduleInstanceDate` 有值 定期交易:
            - **觸發:** 執行 編輯/刪除邏輯
            - **定義:** 參見 `no6_5_recurring_transaction_spec`
    - **成功:**
        - **導航:** 關閉畫面, 返回前一頁
- **刪除邏輯:**
    - **條件:** 僅 編輯模式 可用
    - **觸發:** 點擊 刪除按鈕
    - **檢查:** 該筆交易 `scheduleInstanceDate` 是否有值
    - **IF** `scheduleInstanceDate` 為 null 普通交易:
        - **行為:** 軟刪除 本機 DB 該筆 `Transaction`
        - **欄位:** 必須設定 `deletedOn` 並更新 `updatedOn`
    - **IF** `scheduleInstanceDate` 有值 定期交易:
        - **觸發:** 執行 編輯/刪除邏輯
        - **定義:** 參見 `no6_5_recurring_transaction_spec`
    - **成功:**
        - **導航:** 關閉畫面, 返回前一頁

---

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

---

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