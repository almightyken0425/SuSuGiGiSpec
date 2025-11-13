# 類別編輯器畫面 (CategoryEditorScreen)

_(本文件定義新增/編輯「類別」畫面的 UI、流程與邏輯)_

## 畫面目標 (Screen Objective)

- 提供一個統一的介面，讓使用者可以**新增**一個新類別，或**編輯**一個現有類別的名稱與圖示。
- 確保所有自訂類別都映射到一個標準類別，以便於報表聚合。

## UI 佈局與元件 (UI Layout & Components)

- **頂部導航列 (Top Navigation Bar):**
    - **左側:** 「關閉」或「取消」按鈕。
    - **中間:**
        - **UI:** 顯示靜態標題。
        - **邏輯:** 標題根據進入畫面的模式和類型而變化，例如「新增支出類別」、「編輯收入類別」。
    - **右側:** 「儲存」按鈕，僅在所有必填欄位都有效時才可點擊。

- **核心欄位區 (Core Fields Area):**
    - **類別名稱 (`name`):**
        - **UI:** 一個文字輸入框 (`TextInput`)。此為**必填項**。
    - **圖示 (`icon`):**
        - **UI:** 一個顯示當前所選圖示的區域，點擊後導航至圖標選擇器畫面 (`IconPickerScreen`)。此為**必填項**。
    - **標準類別映射 (`standardCategoryId`):**
        - **UI:** 一個選擇器，點擊後彈出 `StandardCategory.json` 中對應 `categoryType` 的標準類別列表。
        - **邏輯:** 使用者必須選擇一個標準類別進行映射。此為**必填項**。

- **停用開關區 (Disable Switch Area):**
    - **UI:** 一個開關 (Switch) 元件，標題為「停用此類別」。
    - **邏輯:**
        - 僅在「編輯」模式下顯示。
        - 讀取 `disabledOn` 欄位狀態來決定開關的預設值（`null` 為 Off，有時間戳記為 On）。

- **刪除按鈕區 (Delete Button Area):**
    - **UI:** 紅色的「刪除此類別」按鈕，僅在「編輯」模式下顯示。

## 核心邏輯

- **模式判斷 (Mode Detection):**
    - 畫面載入時，檢查導航參數中是否傳入 `categoryId`。
    - **若有 `categoryId` (編輯模式):** 從「**本機資料庫 (Local DB)**」讀取該類別的資料並填入表單。
    - **若無 `categoryId` (新增模式):** 表單為空白，`categoryType` 預設為「支出」。

- **儲存邏輯 (Save Logic):**
    - **新增模式:**
        - **(付費牆檢查)** 檢查「**本機狀態 (e.g., PremiumContext)**」中的 `isPremiumUser` 狀態以及「**本機資料庫**」中的類別數量 (10個，含預設)。若已達上限，則導航至 `PaywallScreen` 而非儲存。
        - 若未達上限，則在「**本機資料庫 (Local DB)**」建立新記錄（**必須**設定 `updatedOn` 時間戳記）。
    - **編輯模式:**
        - 組合表單資料（包含 `name`, `icon`, `standardCategoryId` 以及 `disabledOn` 狀態）。
        - 若「停用開關」被開啟，`disabledOn` 應設為當前時間戳記。
        - 若「停用開關」被關閉，`disabledOn` 應設為 `null`。
        - 更新「**本機資料庫 (Local DB)**」中的該筆記錄（**必須**更新 `updatedOn` 時間戳記）。
    - 儲存成功後，關閉畫面並導航返回類別列表畫面 (`CategoryListScreen`)。

- **刪除邏輯 (Delete Logic):**
    - 點擊「刪除」按鈕時，彈出確認對話框。
    - 使用者確認後，在「**本機資料庫 (Local DB)**」中軟刪除該筆 `Category`（**必須**設定 `deletedOn` 並更新 `updatedOn`，以觸發「批次同步規格」的同步）。
    - 刪除成功後，關閉畫面並導航返回類別列表畫面 (`CategoryListScreen`)。

## 狀態管理 (State Management)

- 使用 `useState` 或表單管理庫來管理以下狀態：
    - `name: string`
    - `iconId: number`
    - `standardCategoryId: number | null`
    - `isDisabled: boolean` (綁定到「停用開關」，預設為 `false`)

## 導航 (Navigation)

- **進入:** 從類別列表畫面 (`CategoryListScreen`) 的「新增」按鈕或列表項目點擊進入。
- **退出:** 點擊「關閉/取消」按鈕，或在「儲存/刪除」成功後，呼叫 `navigation.goBack()`。
