# 轉帳編輯器畫面 (TransferEditorScreen)

_(本文件定義新增/編輯「轉帳」畫面的 UI、流程與邏輯)_

## 畫面目標 (Screen Objective)

- 提供一個統一的介面，讓使用者可以**新增**、**編輯**或**刪除**一筆「轉帳」記錄。
- 支援**同幣別**轉帳與**跨幣別**轉帳 _[付費功能]_。
- 作為建立**定期轉帳**排程的入口 _[付費功能]_。
- 處理編輯由定期排程所產生的轉帳時的特殊邏輯。

## UI 佈局與元件 (UI Layout & Components)

- **頂部導航列 (Top Navigation Bar):**
    - **左側:** 「關閉」或「取消」按鈕。
    - **中間:** 畫面標題，顯示「轉帳」。
    - **右側:**
        - **定期交易按鈕:** 一個循環圖示的按鈕。
        - **邏輯:**
            - **(付費牆檢查)** 點擊時，檢查「**本機狀態 (e.g., PremiumContext)**」中的 `isPremiumUser` 狀態。
            - **若為免費版使用者:** 導航至 `PaywallScreen`。
            - **若為付費版使用者:** 開啟 `ScheduleModal` 進行設定。

- **日期選擇區 (Date Area):**
    - **元件:** `DatePicker`。
    - **邏輯:** 點擊後開啟日期選擇器。此為**必填項**。

- **帳戶選擇區 (Account Selection Area):**
    - **UI:** 左右並排的兩個帳戶選擇器，中間有一個向右的箭頭圖示。
    - **項目:**
        - **左側 (轉出帳戶):**
            - **元件:** `AccountSelector`。
            - **邏輯:** 列表應按 `sortOrder` 排序。選擇後返回 `accountFromId`。此為**必填項**。
        - **右側 (轉入帳戶):**
            - **元件:** `AccountSelector`。
            - **邏輯:** 列表應按 `sortOrder` 排序。選擇後返回 `accountToId`。此為**必填項**。
    - **防呆邏輯:**
        - 當使用者選擇的「轉出帳戶」與「轉入帳戶」相同時，兩個帳戶選擇器應顯示錯誤狀態（例如紅色邊框）。

- **備註區 (Note Area):**
    - **UI:** 一個簡單的文字輸入框。

- **金額輸入區 (Amount Entry Area):**
    - **UI:** 上下垂直排列的金額輸入框 (`TextInput`)。
    - **項目:**
        - **轉出金額 (Amount From):**
            - **UI:** 一個大型的金額輸入框。點擊後彈出原生數字鍵盤。此為**必填項**。
        - **匯率與箭頭 (Rate & Arrow):**
            - **UI:** 僅在**跨幣別轉帳**時顯示。一個向下的箭頭圖示，旁邊顯示即時計算的隱含匯率 (e.g., "1 USD = 32.5 TWD")。
        - **轉入金額 (Amount To):**
            - **UI:** 一個大型的金額輸入框。點擊後彈出原生數字鍵盤。
            - **邏輯:**
                - **同幣別轉帳:** 此欄位**不顯示**。儲存時，`amountToCents` 的值自動等於 `amountFromCents`。
                - **跨幣別轉帳 ([付費功能]):** 此欄位顯示並可編輯，允許使用者輸入實際收到的金額。

- **表單提交區 (Form Submission Area):**
    - **UI:**
        - **刪除按鈕:** 紅色的「刪除此轉帳」按鈕，僅在「編輯」模式下顯示。
        - **儲存按鈕:** 主要顏色的「儲存」按鈕。僅在所有必填欄位都有效，**且轉出/轉入帳戶不同**時才可點擊。

## 核心邏輯

- **模式判斷與預設值 (Mode Detection & Defaults):**
    - 畫面載入時，檢查導航參數中是否傳入 `transferId`。
    - **若有 `transferId` (編輯模式):**
        - 從「**本機資料庫 (Local DB)**」中讀取該筆轉帳的完整資料，填入表單。
        - 顯示「刪除按鈕」。
    - **若無 `transferId` (新增模式):**
        - **日期預設值:** 遵循 `TransactionEditorScreen` 的邏輯，檢查 `defaultDate` 參數，否則為今天。
        - **帳戶預設值:**
            - 「轉出帳戶」應預選 `sortOrder` 最高的項目。
            - 「轉入帳戶」應預選 `sortOrder` 第二高的項目 (若存在)。
            - 若使用者僅有少於 2 個帳戶，則「轉入帳戶」留空，且「儲存」按鈕應為禁用狀態。

- **儲存邏輯 (Save Logic):**
    - 點擊「儲存」按鈕時，組合表單所有狀態 (按鈕的可點擊狀態已完成驗證)。
    - **新增模式:**
        - **跨幣別匯率記錄:** 若偵測到為跨幣別轉帳 (轉出與轉入帳戶的幣別不同)，執行以下操作：
            - 從 `amountFromCents`, `accountFromId` (取得幣別), `amountToCents`, `accountToId` (取得幣別) 中取得所需資訊。
            - 計算出隱含匯率 (`rateCents`)。
            - 在儲存轉帳的同一個批次 (batch) 操作中，呼叫在「**本機資料庫 (Local DB)**」中新增一筆 `CurrencyRates` 記錄（**必須**設定 `updatedOn` 時間戳記）。，將此匯率存入 `CurrencyRates` 表，並將 `rateDate` 設為該筆轉帳的 `transactionDate`。
            - 此操作為付費功能，執行前需檢查「**本機狀態 (e.g., PremiumContext)**」中的 `isPremiumUser` 狀態。若為免費版，應導航至付費牆畫面 (`PaywallScreen`)。

        - **如果未設定重複規則:** 直接在「**本機資料庫 (Local DB)**」建立一筆新記錄（**必須**設定 `updatedOn` 時間戳記）。
        - **如果設定了重複規則 ([付費功能]):**
            - 在「**本機資料庫 (Local DB)**」建立一筆 `Schedules` 記錄（**必須**設定 `updatedOn`），並**立即**為 `startOn` 日期產生第一筆轉帳實例（同樣寫入本機）。
    - **編輯模式:**
        - **檢查是否為定期交易產生:** 檢查該筆轉帳的 `scheduleId` 是否有值。
        - **普通轉帳:** 直接更新「**本機資料庫 (Local DB)**」中的該筆記錄（**必須**更新 `updatedOn` 時間戳記）。
        - **定期轉帳產生:**
            - 彈出對話框，提供選項：「僅此一筆」、「此筆及未來所有」。
            - **「僅此一筆」:** 直接修改當前這筆 `Transfer`。
            - **「此筆及未來所有」:** 在「**本機資料庫 (Local DB)**」中更新原 `Schedule` 的 `endOn`（需更新 `updatedOn`），並建立一個新的 `Schedule` 記錄（也需設定 `updatedOn`）。
    - 儲存成功後，關閉畫面並導航返回前一頁。

- **刪除邏輯 (Delete Logic):**
    - 僅在「編輯」模式下可用。
    - **普通轉帳:** 直接在「**本機資料庫 (Local DB)**」中軟刪除該筆 `Transfer`（**必須**設定 `deletedOn` 並更新 `updatedOn`，以觸發「批次同步規格」的同步）。
    - **定期轉帳產生:**
        - 彈出對話框，提供選項：「僅此一筆」、「此筆及未來所有」。
        - **「僅此一筆」:** 同上，軟刪除當前的 `Transfer` 記錄（更新 `deletedOn` 和 `updatedOn`）。
        - **「此筆及未來所有」:** 在「**本機資料庫 (Local DB)**」中更新原 `Schedule` 的 `endOn`（**必須**更新 `updatedOn` 以觸發同步）。

## 狀態管理 (State Management)

- 使用 `useState` 或表單管理庫來管理以下狀態：
    - `accountFromId: string | null`
    - `accountToId: string | null`
    - `amountFromCents: bigint`
    - `amountToCents: bigint`
    - `transactionDate: number`
    - `note: string`
    - `schedule: Schedule | null`

## 導航 (Navigation)

- **進入:**
    - 從 `HomeScreen` 的 FAB 或列表項點擊進入。
    - 可選參數:
        - `transferId?: string` (用於編輯模式)
        - `defaultDate?: number` (用於預設日期)
- **退出:**
    - 點擊「關閉/取消」按鈕，或在「儲存/刪除」成功後，呼叫 `navigation.goBack()`。
