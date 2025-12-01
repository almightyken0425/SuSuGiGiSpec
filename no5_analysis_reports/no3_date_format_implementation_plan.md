# 日期顯示規範實作計畫

---

## 變更目標

- **建立:** 統一的 智慧日期顯示規範 Locale Aware Smart Format
- **自動化:** 依據裝置系統語系自動適配
- **一致性:** 定義技術層面的統一工具函式

---

## 使用者審閱

> [!IMPORTANT]
> **規範確認**
> - **策略:** 跟隨系統語系 Locale Aware 且不提供手動切換
> - **技術實作:** 封裝全域函式 formatAppDate
> - **模式:** 支援 4 種標準格式 Date, DateWithYear, DateWithoutYear, MonthYear, Year

### 支援格式 Supported Formats

#### Date Without Year
- **用途:** 列表、日期範圍的起迄點
- **範例:** `Oct 25` / `10月25日`
- **Intl 設定:** `{ month: 'short', day: 'numeric' }`

#### Date With Year
- **用途:** 編輯器、單日標題、跨年顯示
- **範例:** `Oct 25, 24` / `24年10月25日` 使用2位數年份
- **Intl 設定:** `{ year: '2-digit', month: 'short', day: 'numeric' }`

#### Month With Year
- **用途:** 月份標題
- **範例:** `Oct 24` / `24年10月` 使用2位數年份
- **Intl 設定:** `{ year: '2-digit', month: 'short' }`

#### Year
- **用途:** 年份標題
- **範例:** `2024` / `2024年` 維持4位數
- **Intl 設定:** `{ year: 'numeric' }`

---

## 預計變更

### 設計系統 no5_design_system

> [!IMPORTANT]
> **文件撰寫規範**
> 所有修改或新增的文件內容，嚴禁使用括號 () 以及編號列表 1. 2. 3.
> 補充說明請直接整合至語句中，列表請一律使用無序列表符號 -

#### [NEW] [no3_date_format_policy.md](file:///C:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no5_design_system/no3_date_format_policy.md)
- 建立新文件定義日期格式策略
- 定義 formatAppDate 工具函式與 Intl DateTimeFormat 的使用方式

### 螢幕規格 no2_screens

#### [MODIFY] [no2_home_screen.md](file:///C:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no2_home_screen.md)
- **原因:** 列表顯示需更新為 Date Without Year
- **動作:** 更新 Wireframe 與 Core Logic
- **新增:** 依據 HomeFilterScreen 選擇的時間粒度定義標題格式
    - **Day:** 使用 Date With Year 如 Oct 25, 24
    - **Week:** 顯示範圍，使用 Date Without Year 如 Oct 20 - Oct 26
    - **Month:** 使用 Month With Year 如 Oct 24
    - **Year:** 使用 Year 如 2024
    - **All:** 顯示範圍，使用 Date With Year 如 Oct 01, 23 - Dec 31, 24 取第一筆與最後一筆非刪除紀錄之日期

#### [MODIFY] [no4_transaction_editor_screen.md](file:///C:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no4_transaction_editor_screen.md)
- **原因:** 編輯器需使用精確格式
- **動作:** 更新 Wireframe 中的日期顯示為 Date With Year

#### [MODIFY] [no5_transfer_editor_screen.md](file:///C:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no5_transfer_editor_screen.md)
- **原因:** 編輯器需使用精確格式
- **動作:** 更新 Wireframe 中的日期顯示為 Date With Year

#### [MODIFY] [no15_search_screen.md](file:///C:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no15_search_screen.md)
- **原因:** 搜尋結果列表需使用 Date Without Year
- **動作:** 更新 Wireframe 中的日期顯示

#### [MODIFY] [no12_currency_rate_list_screen.md](file:///C:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no12_currency_rate_list_screen.md)
- **原因:** 匯率更新時間需符合規範
- **動作:** 檢查並更新日期顯示格式

#### [MODIFY] [no13_currency_rate_editor_sreen.md](file:///C:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no13_currency_rate_editor_sreen.md)
- **原因:** 歷史匯率編輯可能涉及日期
- **動作:** 檢查並更新日期顯示格式

#### [MODIFY] [no16_import_screen.md](file:///C:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no3_accounting_app/no2_screens/no16_import_screen.md)
- **原因:** 匯入預覽列表需使用 Date Without Year
- **動作:** 更新 Wireframe 中的日期顯示

---

## 驗證計畫

### 手動驗證

#### 文件審閱
- **檢查:** 確認 no3_date_format_policy.md 包含技術實作細節
- **檢查:** 檢查 no2_home_screen.md 是否與規範視覺一致
- **檢查:** 檢查所有修改過的檔案是否符合日期顯示規範
