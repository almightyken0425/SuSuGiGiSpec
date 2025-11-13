# 帳戶編輯器畫面 (AccountEditorScreen)

_(本文件定義新增/編輯「帳戶」畫面的 UI、流程與邏輯)_

## 畫面目標 (Screen Objective)

- 提供一個統一的介面，讓使用者可以**新增**一個新帳戶，或**編輯**一個現有帳戶的名稱、圖示等屬性。
- 處理新增外幣帳戶時的匯率輸入流程 _[付費功能]_。

## UI 佈局與元件 (UI Layout & Components)

此畫面通常以 Modal 形式從底部彈出，佔據整個螢幕。

- **頂部導航列 (Top Navigation Bar):**
    - **左側:** 「關閉」或「取消」按鈕。
    - **中間:** 畫面標題，根據模式顯示「新增帳戶」或「編輯帳戶」。
    - **右側:** 「儲存」按鈕，僅在所有必填欄位都有效時才可點擊。

- **核心欄位區 (Core Fields Area):**
    - **帳戶名稱 (`name`):**
        - **UI:** 一個文字輸入框 (`TextInput`)。此為**必填項**。
    - **圖示 (`icon`):**
        - **UI:** 一個顯示當前所選圖示的區域，點擊後導航至圖標選擇器畫面 (`IconPickerScreen`)。此為**必填項**。
    - **幣別 (`CurrencyId`):**
        - **UI:** 一個選擇器，點擊後彈出貨幣列表 (`Currency.json`)。
        - **邏輯:** 在「編輯」模式下，此欄位**不可修改**。在「新增」模式下，若選擇非基礎貨幣，需觸發匯率輸入流程。此為**必填項**。
    - **初始餘額 (`initialBalanceCents`):**
        - **UI:** 一個金額輸入框。
        - **邏輯:** 此欄位**僅在「新增」模式下顯示**。
    - **標準帳戶類型 (`standardAccountTypeId`):**
        - **UI:** 一個選擇器，點擊後彈出 `StandardAccountType.json` 的列表。
        - **邏輯:** 允許使用者將帳戶歸類 (例如：現金、銀行、投資)。

- **停用開關區 (Disable Switch Area):**
    - **UI:** 一個開關 (Switch) 元件，標題為「停用此帳戶」。
    - **邏輯:**
        - 僅在「編輯」模式下顯示。
        - 讀取 `disabledOn` 欄位狀態來決定開關的預設值（`null` 為 Off，有時間戳記為 On）。

- **刪除按鈕區 (Delete Button Area):**
    - **UI:** 紅色的「刪除此帳戶」按鈕，僅在「編輯」模式下顯示。

## 核心邏輯

- **模式判斷 (Mode Detection):**
    - 畫面載入時，檢查導航參數中是否傳入 `accountId`。
    - **若有 `accountId` (編輯模式):** 從「**本機資料庫 (Local DB)**」讀取該帳戶的資料並填入表單。
    - **若無 `accountId` (新增模式):** 準備一個空的表單。

- **儲存邏輯 (Save Logic):**
    - **新增模式:**
        - **(付費牆檢查)** 檢查「**本機狀態 (e.g., PremiumContext)**」中的 `isPremiumUser` 狀態以及「**本機資料庫**」中的帳戶數量 (3個)。若已達上限，則導航至付費牆畫面 (`PaywallScreen`)。
        - **(付費牆檢查 - 多幣別)** 若使用者選擇了非基礎貨幣，檢查「**本機狀態 (e.g., PremiumContext)**」中的 `isPremiumUser` 狀態。若為免費版，導航至 付費牆畫面 (`PaywallScreen`)。
        - **(匯率輸入流程 - 多幣別)** 若使用者為付費版 (從「**本機狀態**」檢查) 且選擇了非基礎貨幣，在儲存前，必須：
            1.  彈出一個對話框或介面，提示使用者輸入該貨幣對基礎貨幣的**初始匯率** (例如 "1 USD = ? TWD")。
            2.  此匯率輸入為**必填項**。
        - **儲存操作:**
            - 若涉及匯率輸入，將該匯率記錄與帳戶資料在一個批次 (batch) 操作中，分別在「**本機資料庫 (Local DB)**」中新增 `CurrencyRates` 和 `Account` 記錄（**兩者都必須**設定 `updatedOn` 時間戳記）。
            - 若不涉及，則直接在「**本機資料庫 (Local DB)**」建立新記錄（**必須**設定 `updatedOn` 時間戳記）。
    - **編輯模式:**
        - 組合表單資料（包含 `name`, `icon` 以及 `disabledOn` 狀態）。
        - 若「停用開關」被開啟，`disabledOn` 應設為當前時間戳記。
        - 若「停用開關」被關閉，`disabledOn` 應設為 `null`。
        - 更新「**本機資料庫 (Local DB)**」中的該筆記錄（**必須**更新 `updatedOn` 時間戳記）。
    - **儲存成功後:** 關閉畫面並導航返回帳戶列表畫面 (`AccountListScreen`)。

- **刪除邏輯 (Delete Logic):**
    - 點擊「刪除」按鈕時，彈出確認對話框。
    - 使用者確認後，在「**本機資料庫 (Local DB)**」中軟刪除該筆 `Account`（**必須**設定 `deletedOn` 並更新 `updatedOn`，以觸發「批次同步規格」的同步）。
    - 刪除成功後，關閉畫面並導航返回帳戶列表畫面 (`AccountListScreen`)。

## 狀態管理 (State Management)

- 使用 `useState` 或表單管理庫來管理以下狀態：
    - `name: string`
    - `iconId: number`
    - `currencyId: number`
    - `initialBalanceCents: bigint`
    - `standardAccountTypeId: number | null`
    - `isDisabled: boolean` (綁定到「停用開關」，預設為 `false`)

## 導航 (Navigation)

- **進入:** 從帳戶列表畫面 (`AccountListScreen`) 的「新增」按鈕或列表項目點擊進入。
- **退出:** 點擊「關閉/取消」按鈕，或在「儲存/刪除」成功後，呼叫 `navigation.goBack()`。
