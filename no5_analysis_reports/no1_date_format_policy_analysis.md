# 日期顯示規範實作計畫

## 目標描述
在記帳 App 中建立統一的「智慧日期顯示規範 (Locale-Aware Smart Format)」。
不提供使用者手動設定，而是依據裝置系統語系自動適配（例如英文顯示 `Oct 25`，繁中顯示 `10月25日`）。
同時定義技術層面的統一工具函式，確保全 App 一致性。

## 需要使用者審閱
> [!IMPORTANT]
> **規範確認:**
> - **策略:** 跟隨系統語系 (Locale-Aware)，不提供手動切換。
> - **技術實作:** 封裝全域函式 `formatAppDate(date, mode)`。
> - **模式:** 僅提供 `short` (列表/標題用) 與 `full` (編輯/詳情用) 兩種模式。

### 格式定義 (Format Definitions)

#### 1. Short Mode (列表/標題用)
*   **用途:** 空間受限的列表、分組標題。
*   **邏輯:** `month: 'short', day: 'numeric'` (當年隱藏年份)。
*   **範例 (en-US):** `Oct 25`
*   **範例 (zh-TW):** `10月25日`

#### 2. Full Mode (編輯/詳情用)
*   **用途:** 需要精確資訊的編輯器、詳情頁。
*   **邏輯:** `year: 'numeric', month: 'short', day: 'numeric'`。
*   **範例 (en-US):** `Oct 25, 2024`
*   **範例 (zh-TW):** `2024年10月25日`

## 預計變更

### 設計系統 (Design System)
#### [NEW] [no3_date_format_policy.md](file:///Users/kenchio/Documents/GitHub/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no5_design_system/no3_date_format_policy.md)
- 建立新文件定義日期格式策略。
- **新增:** 技術實作章節，定義 `formatAppDate` 工具函式與 `Intl.DateTimeFormat` 的使用方式。

### 畫面規格 (Screen Specifications)

#### 需要更新 (Needs Update)

1.  **[MODIFY] [no2_home_screen.md](file:///Users/kenchio/Documents/GitHub/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no2_home_screen.md)**
    *   **原因:** 列表顯示需更新為 `Smart` 格式 (如 `Oct 25`)；邏輯需引用 Policy。
    *   **動作:** 更新 Wireframe 與 Core Logic。

2.  **[MODIFY] [no4_transaction_editor_screen.md](file:///Users/kenchio/Documents/GitHub/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no4_transaction_editor_screen.md)**
    *   **原因:** 編輯器需使用 `Full` 格式 (如 `Oct 25, 2024 (Fri)`) 以確保精確。
    *   **動作:** 更新 Wireframe 中的日期顯示。

3.  **[MODIFY] [no5_transfer_editor_screen.md](file:///Users/kenchio/Documents/GitHub/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no5_transfer_editor_screen.md)**
    *   **原因:** 同上，編輯器需使用 `Full` 格式。
    *   **動作:** 更新 Wireframe 中的日期顯示。

4.  **[MODIFY] [no15_search_screen.md](file:///Users/kenchio/Documents/GitHub/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no15_search_screen.md)**
    *   **原因:** 搜尋結果列表需使用 `Smart` 格式。
    *   **動作:** 更新 Wireframe 中的日期顯示。

5.  **[MODIFY] [no12_currency_rate_list_screen.md](file:///Users/kenchio/Documents/GitHub/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no12_currency_rate_list_screen.md)**
    *   **原因:** 匯率更新時間需符合規範 (可能需定義 Time 顯示，但日期部分應一致)。
    *   **動作:** 檢查並更新日期顯示格式。

6.  **[MODIFY] [no13_currency_rate_editor_sreen.md](file:///Users/kenchio/Documents/GitHub/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no13_currency_rate_editor_sreen.md)**
    *   **原因:** 歷史匯率編輯可能涉及日期。
    *   **動作:** 檢查並更新日期顯示格式。

7.  **[MODIFY] [no16_import_screen.md](file:///Users/kenchio/Documents/GitHub/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no16_import_screen.md)**
    *   **原因:** 匯入預覽列表需使用 `Smart` 格式。
    *   **動作:** 更新 Wireframe 中的日期顯示。

#### 無需更新 (No Update Required)

*   **no1_login_screen.md:** 無日期顯示。
*   **no3_home_filter_screen.md:** 僅選擇時間粒度 (Day/Week/Month)，非具體日期格式。
*   **no6_settings_screen.md:** 選單列表，無日期。
*   **no7_category_list_screen.md:** 類別列表，無日期。
*   **no8_category_editor_screen.md:** 類別編輯，無日期。
*   **no9_account_list_screen.md:** 帳戶列表，無日期。
*   **no10_account_editor_screen.md:** 帳戶編輯，無日期。
*   **no11_icon_picker_screen.md:** 圖示選擇，無日期。
*   **no14_preference_screen.md:** 已移除日期格式設定，無其他日期顯示。
*   **no17_paywall_screen.md:** 訂閱資訊通常由 Store 處理或顯示固定格式 (如 "Renews on...")，暫不強制套用 App Policy。
*   **no18_redeem_code_screen.md:** 兌換結果可能顯示期限，但屬一次性資訊。
*   **no19_theme_settings_screen.md:** 主題設定，無日期。


## 驗證計畫

### 手動驗證
- **文件審閱:** 確認 `no3_date_format_policy.md` 包含技術實作細節。
- **Wireframe 檢查:** 檢查 `no2_home_screen.md` 是否與規範視覺一致。
