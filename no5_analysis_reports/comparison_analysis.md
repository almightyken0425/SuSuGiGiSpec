# 產品定義與會計應用規格比較分析

## 執行摘要

本文件比較 [`no1_product_initiation/no2_product_definition.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no1_product_initiation/no2_product_definition.md) 中定義的 Accounting App User Stories 與 [`no3_module_specs/no1_accounting_app`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app) 中的實際規格文件。

### 關鍵發現

- ✅ **大部分 User Stories 已有對應規格**：核心功能 CRUD、資料同步、儀表板等均已覆蓋
- ⚠️ **部分 User Stories 缺少明確對應**：主題系統、序號兌換等功能在模組規格中尚不完整
- 📊 **規格更詳細**：模組規格提供了比產品定義更精細的 UI/UX 和互動邏輯

---

## 對應關係矩陣

### 交易與自動化 (Transaction & Automation)

| User Story | 產品定義 | 模組規格對應 | 狀態 |
|-----------|--------|------------|------|
| 支出管理 (Expense CRUD) | ✓ | `no2_home_screen.md` + `no3_transaction_editor_screen.md` | ✅ 完整 |
| 收入管理 (Income CRUD) | ✓ | `no3_transaction_editor_screen.md` | ✅ 完整 |
| 轉帳管理 (Transfer CRUD) | ✓ | `no4_transfer_editor_screen.md` | ✅ 完整 |
| 定期交易 (Recurring Transaction) | ✓ (付費功能) | `no3_transaction_editor_screen.md` + `no3_background_logics/no4_recurring_transactions_spec.md` | ✅ 完整 |

### 資產管理 (Asset Management)

| User Story | 產品定義 | 模組規格對應 | 狀態 |
|-----------|--------|------------|------|
| 帳戶管理 (Account CRUD) | ✓ | `no8_account_list_screen.md` + `no9_account_editor_screen.md` | ✅ 完整 |
| 類別管理 (Category CRUD) | ✓ | `no6_category_list_screen.md` + `no7_category_editor_screen.md` | ✅ 完整 |
| 預設資料初始化 (Onboarding Data) | ✓ | `no3_background_logics/no2_post_auth_logic.md` | ✅ 完整 |
| 多幣別支援 (Multi-Currency) | ✓ (付費功能) | `no11_currency_rate_list_screen.md` + `no12_currency_rate_editor_screen.md` + `no4_data_models/no1_data_models.md` | ✅ 完整 |
| 解除限制 (Unlimited Access) | ✓ (付費功能) | 散布於多個畫面的權限檢查邏輯 | ✅ 完整 |

### 資料與同步 (Data & Sync)

| User Story | 產品定義 | 模組規格對應 | 狀態 |
|-----------|--------|------------|------|
| 離線支援 (Offline Architecture) | ✓ | `no2_home_screen.md` 中提及本機 DB 監聽機制 | ✅ 完整 |
| 雲端同步引擎 (Sync Engine) | ✓ (付費功能) | `no3_background_logics/no3_batch_sync_spec.md` | ✅ 完整 |
| 資料匯入 (CSV Import) | ✓ (付費功能) | `no15_import_screen.md` | ✅ 完整 |

### 儀表板與體驗 (Dashboard & Experience)

| User Story | 產品定義 | 模組規格對應 | 狀態 |
|-----------|--------|------------|------|
| 首頁儀表板 (Home Dashboard) | ✓ | `no2_home_screen.md` | ✅ 完整 |
| 搜尋功能 (Local Search) | ✓ | `no14_search_screen.md` | ✅ 完整 |
| 多語言支援 (i18n) | ✓ | `no13_preference_screen.md` (語系設定) | ✅ 完整 |
| 配色主題系統 (Theme System) | ✓ | ❌ 無對應規格 | ⚠️ **缺少** |

以下 User Stories 在模組規格中有完整且詳細的對應：

#### 1.1 核心 CRUD 功能
- **支出/收入管理**：[`no3_transaction_editor_screen.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no2_screens/no3_transaction_editor_screen.md) 提供了非常詳細的介面規格，包含：
  - UI 佈局（Modal 形式、日期選擇、金額輸入）
  - 權限邏輯（付費/免費版差異）
  - 定期交易整合
  - 編輯/刪除邏輯

#### 1.2 資產管理
- **帳戶管理**：[`no8_account_list_screen.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no2_screens/no8_account_list_screen.md) + [`no9_account_editor_screen.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no2_screens/no9_account_editor_screen.md)
- **類別管理**：[`no6_category_list_screen.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no2_screens/no6_category_list_screen.md) + [`no7_category_editor_screen.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no2_screens/no7_category_editor_screen.md)
- 兩者都包含圖標選擇器整合 ([`no10_icon_picker_screen.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no2_screens/no10_icon_picker_screen.md))

#### 1.3 背景邏輯與同步
- **定期交易**：[`no4_recurring_transactions_spec.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no3_background_logics/no4_recurring_transactions_spec.md) 詳細定義了：
  - 建立邏輯
  - 補產生邏輯（App 啟動時）
  - 編輯/刪除邏輯（僅此一筆 vs. 此筆及未來所有）
  
- **雲端同步**：[`no3_batch_sync_spec.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no3_background_logics/no3_batch_sync_spec.md)

#### 1.4 資料模型
- [`no1_data_models.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no4_data_models/no1_data_models.md) 完整定義了：
  - 使用者自訂資料結構（Books, Accounts, Categories, Transactions, Transfers, CurrencyRates, Schedules, Settings）
  - App 標準定義資料（StandardCategory, StandardAccountType, IconDefinition, Currencies）
  - 時間格式標準

---

### 2. 缺少或不完整的功能

以下 User Stories 在模組規格中缺少明確對應或僅有部分覆蓋：

#### 2.1 主題系統 (Theme System)

> [!WARNING]
> **產品定義包含三個相關 User Stories，但模組規格中完全沒有對應**

產品定義中提到：
- **配色主題系統 (Theme System)**：建立設計代幣與變數架構
- **主題切換介面 (Theme Switcher)**：使用者可在設定中切換配色主題
- **新增配色主題 (New Theme)**：設計團隊新增配色組合

**缺少內容：**
- ❌ 無主題系統的資料模型定義
- ❌ 無主題切換的 UI 規格
- ❌ 無設計代幣 (Design Tokens) 定義文件

#### 2.2 序號兌換系統 (Redeem System)

> [!WARNING]
> **產品定義包含三個相關 User Stories，但模組規格中完全沒有對應**

產品定義中提到：
- **序號驗證系統 (Redeem System)**：後端序號生成與驗證系統
- **序號兌換介面 (Redeem UI)**：使用者在設定中輸入序號
- **序號管理工具 (Redeem Management)**：營運團隊生成和管理序號

**缺少內容：**
- ❌ 無序號兌換的 UI 畫面規格
- ❌ 無序號資料模型定義（如 RedeemCodes 表）
- ❌ 無序號驗證邏輯規格
- ❌ 無序號管理工具規格

**備註：** 雖然 [`no16_paywall_screen.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no2_screens/no16_paywall_screen.md) 存在，但該畫面通常用於付費訂閱導購，與序號兌換機制不同。


---

### 3. 模組規格比產品定義更詳細的部分

模組規格在以下方面提供了比產品定義更豐富的細節：

#### 3.1 複雜的 UI 互動邏輯

**首頁儀表板** ([`no2_home_screen.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no2_screens/no2_home_screen.md)) 包含：
- 圓餅圖動態合併邏輯（前 7 類別，自動合併為"其他"）
- 折疊/展開動畫（向上滾動時收合圓餅圖）
- 時間區間切換的分頁架構
- 報表篩選的 Bottom Sheet Modal

**產品定義僅提到：**
> 作為使用者，我想要在首頁查看當月收支摘要與列表，以便快速掌握財務狀況。

#### 3.2 權限邏輯細節

模組規格詳細定義了免費版與付費版的功能差異：
- 免費版限制：最多 3 個帳戶、10 個類別
- 付費功能檢查時機（點擊時檢查 `PremiumContext.isPremiumUser`）
- 拒絕存取時的 UI 提示（顯示 Dialog，導航至 PaywallScreen）

#### 3.3 資料同步時間戳機制

[`no1_data_models.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no4_data_models/no1_data_models.md) 明確規定：
- 所有時間欄位儲存為 **UTC Unix Timestamp 毫秒**
- 所有計算與顯示基於使用者設定的 **主要時區 `timeZone`**
- 軟刪除機制使用 `deletedOn` 欄位

#### 3.4 認證與初始化流程

背景邏輯規格提供了完整的流程：
- [`no1_app_bootstrap_flow.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no3_background_logics/no1_app_bootstrap_flow.md)：App 啟動流程
- [`no2_post_auth_logic.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no3_background_logics/no2_post_auth_logic.md)：登入認證後邏輯（包含預設資料初始化）

---

## 建議行動

### 優先級 1: 補充缺失規格

#### 主題系統
建議新增以下文件：
- `no3_module_specs/no1_accounting_app/no2_screens/noXX_theme_settings_screen.md`
- `no3_module_specs/no1_accounting_app/no5_design_system/no1_theme_tokens.md`

應包含：
- 主題資料模型（Themes 表或 JSON 定義）
- 主題切換 UI（在 PreferenceScreen 或 SettingsScreen 中）
- 設計代幣定義（顏色、字型、間距等）

#### 序號兌換系統
建議新增以下文件：
- `no3_module_specs/no1_accounting_app/no2_screens/noXX_redeem_code_screen.md`
- `no3_module_specs/no1_accounting_app/no3_background_logics/noXX_redeem_code_validation.md`

應包含：
- RedeemCodes 資料模型
- 序號兌換 UI 規格
- 序號驗證邏輯（包含 Tier 映射）


### 優先級 2: 保持一致性

#### 同步產品定義與模組規格
- 當產品定義修改時，應同步更新對應的模組規格
- 當新增 User Story 時，應規劃對應的模組規格文件

#### 建立對應關係文件
建議在 `no3_module_specs/no1_accounting_app/` 下新增：
- `no0_user_story_mapping.md`：明確列出每個 User Story 與對應規格的映射

### 優先級 3: 驗證實作覆蓋度

建議建立檢查清單：
- [ ] 每個 User Story 是否有對應的 UI 規格？
- [ ] 每個付費功能是否有明確的權限檢查邏輯？
- [ ] 每個背景邏輯是否有對應的資料模型支援？
- [ ] 每個畫面是否定義了導航關係？

---

## 總結

| 類別 | 完整覆蓋 | 部分覆蓋 | 缺少規格 |
|------|---------|---------|---------|
| 交易與自動化 | 4 | 0 | 0 |
| 資產管理 | 5 | 0 | 0 |
| 資料與同步 | 3 | 0 | 0 |
| 儀表板與體驗 | 3 | 0 | 6 |
| **總計** | **18** | **0** | **6** |

**覆蓋率統計：**
- 完整覆蓋：75%（18/24）
- 缺少規格：25%（6/24）

**結論：**
`no1_accounting_app` 模組規格對核心功能（CRUD、資產管理、資料同步）有非常完整且詳細的定義，甚至超越了產品定義的描述深度。然而，在進階功能（主題系統、序號兌換）方面存在明顯缺口。建議優先補充這些缺失的規格文件，以確保產品定義與實作規格的完整對應。
