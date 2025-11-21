# 配色主題系統規格補齊待辦清單

## 現況說明

產品定義 ([no2_product_definition.md](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no1_product_initiation/no2_product_definition.md)) 包含三個相關 User Stories：

1. **配色主題系統 (Theme System)**: 作為開發團隊，我想要建立設計代幣與變數架構，以便 App 可支援多套配色主題。
2. **主題切換介面 (Theme Switcher)**: 作為使用者，我想要在設定中切換不同的配色主題，以便客製化我的介面外觀。
3. **新增配色主題 (New Theme)**: 作為設計團隊，我想要為系統新增一套完整的配色組合，以便提供使用者更多選擇。

**問題**: `no3_module_specs/no1_accounting_app` 中完全沒有對應的規格文件。

---

## 待補充規格清單

### 優先級 1: 設計系統基礎

#### [ ] 1.1 設計代幣定義文件
**檔案路徑**: `no3_module_specs/no1_accounting_app/no5_design_system/no1_design_tokens.md`

**應包含內容**:
- Color Tokens
  - Primary colors (品牌主色)
  - Secondary colors (輔助色)
  - Semantic colors (Success, Warning, Error, Info)
  - Neutral colors (Background, Surface, Border, Text)
- Typography Tokens
  - Font families
  - Font sizes
  - Font weights
  - Line heights
- Spacing Tokens
  - 間距系統 (4px, 8px, 12px, 16px, 24px, 32px...)
- 其他 Tokens
  - Border radius
  - Shadows
  - Opacity levels

#### [ ] 1.2 主題資料模型
**檔案路徑**: `no3_module_specs/no1_accounting_app/no4_data_models/no1_data_models.md` (擴充)

**應新增**:
- Settings 表新增 `settingKey: 'currentThemeId'`
- 定義主題 JSON 結構或 Themes 表結構
  - `id`: String, 主題唯一識別碼
  - `name`: String, 主題顯示名稱
  - `colorTokens`: Object, 色彩代幣映射
  - `isBuiltIn`: Boolean, 是否為內建主題
  - `createdOn`: Number, Unix Timestamp ms

---

### 優先級 2: UI 規格

#### [ ] 2.1 主題切換畫面規格
**檔案路徑**: `no3_module_specs/no1_accounting_app/no2_screens/no17_theme_settings_screen.md`

**應包含內容**:
- **UI 佈局**:
  - 主題預覽卡片列表
  - 每個卡片顯示主題名稱與色彩預覽
  - 當前選中主題的標記
- **互動邏輯**:
  - 點擊卡片立即切換主題
  - 即時預覽效果（或延遲應用）
- **導航**:
  - 從 PreferenceScreen 進入
  - 回退邏輯

#### [ ] 2.2 偏好設定畫面更新
**檔案路徑**: `no3_module_specs/no1_accounting_app/no2_screens/no13_preference_screen.md` (修改)

**應新增**:
- 新增「配色主題」選項
- 顯示當前主題名稱
- 點擊後導航至 ThemeSettingsScreen

---

### 優先級 3: 背景邏輯

#### [ ] 3.1 主題載入與切換邏輯
**檔案路徑**: `no3_module_specs/no1_accounting_app/no3_background_logics/no5_theme_management.md`

**應包含內容**:
- **主題載入流程**:
  - App 啟動時讀取 `currentThemeId`
  - 從本機或遠端載入主題定義
  - 應用主題到 App 全域
- **主題切換流程**:
  - 更新 Settings 表
  - 觸發 UI 重新渲染
  - 持久化選擇
- **預設主題處理**:
  - 首次啟動時的預設主題
  - 系統主題跟隨邏輯（可選）

#### [ ] 3.2 內建主題定義
**檔案路徑**: `no3_module_specs/no1_accounting_app/no5_design_system/no2_built_in_themes.md`

**應包含內容**:
- 至少定義 2-3 套內建主題
  - Light Theme (淺色主題)
  - Dark Theme (深色主題)
  - 可選: Colorful Theme (高對比主題)
- 每套主題的完整 Token 映射

---

### 優先級 4: 擴展性設計

#### [ ] 4.1 自訂主題規格 (可選，未來功能)
**檔案路徑**: `no3_module_specs/no1_accounting_app/no2_screens/no18_custom_theme_editor_screen.md`

**應包含內容**:
- 允許使用者建立自訂主題
- 色彩選擇器 UI
- 預覽功能
- 儲存與管理自訂主題

#### [ ] 4.2 主題分享/匯入 (可選，未來功能)
**檔案路徑**: `no3_module_specs/no1_accounting_app/no3_background_logics/no6_theme_import_export.md`

**應包含內容**:
- 匯出主題為 JSON
- 從分享連結或檔案匯入主題
- 主題驗證邏輯

---

## 規格撰寫順序建議

1. **設計代幣定義** → 撰寫 `no1_design_tokens.md`
2. **內建主題定義** → 撰寫 `no2_built_in_themes.md`
3. **主題資料模型** → 更新 `no1_data_models.md`
4. **主題切換畫面** → 撰寫 `no17_theme_settings_screen.md`
5. **主題管理邏輯** → 撰寫 `no5_theme_management.md`

---

## 參考資料

- [Material Design - Color System](https://m3.material.io/styles/color/system/overview)
- [Design Tokens - W3C Community Group](https://design-tokens.github.io/community-group/format/)
- [iOS Human Interface Guidelines - Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode)

---

## 驗收標準

- [ ] 所有清單中的規格文件已建立
- [ ] 設計代幣文件包含完整的 Token 定義
- [ ] 內建主題文件定義了 Light/Dark 兩套主題的 Token 映射
- [ ] UI 規格文件包含完整的互動邏輯與導航流程
- [ ] 背景邏輯文件清楚定義了主題載入與切換的技術流程
