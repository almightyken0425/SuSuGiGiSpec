# 交易編輯器畫面 (TransactionEditorScreen)

_(本文件定義新增/編輯「收支」交易畫面的 UI、流程與邏輯)_

## 畫面目標 (Screen Objective)

- 提供一個目標明確的介面，讓使用者可以**新增**、**編輯**或**刪除**一筆「收入」或「支出」交易。
- 作為建立**定期收支**排程的入口。
- 處理編輯由定期排程所產生的交易時的特殊邏輯。

## UI 佈局與元件 (UI Layout & Components)

此畫面通常以 Modal 形式從底部彈出，佔據整個螢幕。

- **頂部導航列 (Top Navigation Bar):**
    - **左側:** 「關閉」或「取消」按鈕。
    - **中間 (靜態標題):**
        - **UI:** 根據導航傳入的 `type` 參數與模式，靜態顯示「新增支出」、「新增收入」、「編輯支出」或「編輯收入」。
        - **邏輯:** 此標題不可點擊。
    - **右側:**
        - **定期交易按鈕:** 一個循環圖示的按鈕。
        - **邏輯:**
            - **(付費牆檢查)** 點擊時，檢查「**本機狀態 (e.g., PremiumContext)**」中的 `isPremiumUser` 狀態。
            - **若為免費版使用者:** 導航至 `PaywallScreen`。
            - **若為付費版使用者:** 開啟 `ScheduleModal` 進行設定。

- **日期選擇區 (Date Area):**
    - **位置:** 位於導航列正下方。
    - **元件:** `DatePicker.tsx`。
    - **邏輯:** 點擊後開啟日期選擇器。此為**必填項**。

- **金額輸入區 (Amount Entry Area):**
    - **位置:** 位於日期選擇區下方。
    - **UI:** 一個大型的金額**輸入框** (`TextInput`)。點擊後會彈出**作業系統原生的數字鍵盤 (numpad)**。
    - **邏輯:** 輸入的數值會直接更新至 `amountCents` 狀態。應設定 `keyboardType` 為 `decimal-pad` 或 `numeric`。

- **核心欄位區 (Core Fields Area):**
    - **位置:** 位於金額顯示區下方。
    - **UI:** 一個列表。
    - **項目:**
        - **類別 (Category):**
            - **元件:** `CategorySelector`。
            - **UI:** 可以是滾輪選擇器 (Wheel Picker)。若類別過多，點擊後應彈出 Modal 列表供使用者搜尋和選擇。
            - **邏輯:** 列表會根據導航傳入的 `type` 參數 (`income`/`expense`) 進行過濾。選擇後返回 `categoryId`。此為**必填項**。
        - **帳戶 (Account):**
            - **元件:** `AccountSelector.tsx`。
            - **UI:** 同上，可以是滾輪選擇器或彈出 Modal。
            - **邏輯:** 帳戶按 `sortOrder` 排序。選擇後返回 `accountId`。此為**必填項**。
        - **備註 (Note):**
            - **UI:** 一個簡單的文字輸入框。
            - **邏輯:** 允許使用者輸入文字，對應 `Transactions` 表的 `note` 欄位。

- **表單提交區 (Form Submission Area):**
    - **位置:** 位於核心欄位區下方。
    - **UI:**
        - **刪除按鈕:** 紅色的「刪除此交易」按鈕，僅在「編輯」模式下顯示。
        - **儲存按鈕:** 主要顏色的「儲存」按鈕，僅在所有必填欄位都有效時才可點擊。

## 核心邏輯

- **模式判斷與預設值 (Mode Detection & Defaults):**
    - 畫面載入時，檢查導航參數中是否傳入 `transactionId`。
    - **若有 `transactionId` (編輯模式):**
        - 從「**本機資料庫 (Local DB)**」中讀取該筆交易的完整資料，填入表單。
        - 標題應顯示為「編輯支出」或「編輯收入」。
        - 顯示「刪除按鈕」。
    - **若無 `transactionId` (新增模式):**
        - 標題應顯示為「新增支出」或「新增收入」。
        - **日期預設值:**
            - 檢查導航參數中是否傳入 `defaultDate` (來自 `HomeScreen` 的報表日期)。若有，則使用該日期。
            - 若無，則預設為「今天」(基於使用者裝置時區)。
        - **其他預設值:** **類別**與**帳戶**皆應預選其列表中 `sortOrder` 最高（數字最小）的項目。

- **儲存邏輯 (Save Logic):**
    - 點擊「儲存」按鈕時，組合表單所有狀態 (`categoryId`, `accountId`, `amountCents` 等) 及導航傳入的 `type`。
    - **新增模式:**
        - **如果未設定重複規則:** 直接在「**本機資料庫 (Local DB)**」建立一筆新記錄（**必須**設定 `updatedOn` 時間戳記）。
        - **如果設定了重複規則:**
            - 在「**本機資料庫 (Local DB)**」建立一筆 `Schedules` 記錄（**必須**設定 `updatedOn`），並**立即**為 `startOn` 日期產生第一筆交易實例（同樣寫入本機）。
    - **編輯模式:**
        - **檢查是否為定期交易產生:** 檢查該筆交易的 `scheduleInstanceDate` 是否有值。
        - **普通交易:** 直接更新「**本機資料庫 (Local DB)**」中的該筆記錄（**必須**更新 `updatedOn` 時間戳記）。
        - **定期交易產生:**
            - 彈出對話框，提供選項：「僅此一筆」、「此筆及未來所有」。
            - **「僅此一筆」:** 直接修改當前這筆 `Transaction`。
            - **「此筆及未來所有」:** 在「**本機資料庫 (Local DB)**」中更新原 `Schedule` 的 `endOn`（需更新 `updatedOn`），並建立一個新的 `Schedule` 記錄（也需設定 `updatedOn`）。
    - 儲存成功後，關閉畫面並導航返回前一頁 (通常是 `HomeScreen`)。

- **刪除邏輯 (Delete Logic):**
    - 僅在「編輯」模式下可用。
    - **檢查是否為定期交易產生:** 檢查該筆交易的 `scheduleInstanceDate` 是否有值。
    - **普通交易:** 直接在「**本機資料庫 (Local DB)**」中軟刪除該筆 `Transaction`（**必須**設定 `deletedOn` 並更新 `updatedOn`，以觸發「批次同步規格」的同步）。
    - **定期交易產生:**
        - 彈出對話框，提供選項：「僅此一筆」、「此筆及未來所有」。
        - **「僅此一筆」:** 軟刪除當前這筆 `Transaction`。
        - **「此筆及未來所有」:** 在「**本機資料庫 (Local DB)**」中更新原 `Schedule` 的 `endOn`（**必須**更新 `updatedOn` 以觸發同步）。
    - 刪除成功後，關閉畫面並導航返回。

## 狀態管理 (State Management)

- **核心參數 (來自導航):**
    - `type: 'expense' | 'income'`
- **使用 `useState` 或表單管理庫來管理以下狀態：**
    - `amountCents: bigint` (來自金額輸入框)
    - `categoryId: string | null` (來自類別選擇器)
    - `accountId: string | null` (來自帳戶選擇器)
    - `transactionDate: number` (來自日期選擇器)
    - `note: string` (來自備註輸入框)
    - `schedule: Schedule | null` (來自定期交易 Modal)

## 導航 (Navigation)

- **進入:**
    - 從 `HomeScreen` 的 Footer 按鈕或列表項點擊進入。
    - **必要參數:**
        - `type: 'income' | 'expense'` (用於決定編輯器模式)
    - **可選參數:**
        - `transactionId?: string` (用於編輯模式)
        - `defaultDate?: number` (用於預設日期，當 `HomeScreen` 粒度為 `daily` 時傳入)
- **退出:**
    - 點擊「關閉/取消」按鈕，或在「儲存/刪除」成功後，呼叫 `navigation.goBack()`。
