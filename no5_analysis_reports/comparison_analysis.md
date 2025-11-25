# 產品定義與會計應用規格比較分析

## 執行摘要

本文件比較 [`no1_product_initiation/no2_product_definition.md`](../../no1_product_initiation/no2_product_definition.md) 中定義的 Accounting App User Stories 與 [`no3_module_specs`](../../no3_module_specs) 中的實際規格文件。

### 關鍵發現 (2025-11-24 最新分析)

- ✅ **100% User Stories 覆蓋率**：Accounting App 的所有使用者故事（包含核心功能、資產管理、體驗優化）皆已有對應的規格文件。
- ✅ **主題與序號系統已補齊**：原先缺失的主題管理與序號兌換介面，已建立完整的規格文件。
- ℹ️ **營運工具採輕量化策略**：序號管理工具（Redeem Management）在 MVP 階段確認使用 Firebase Console 進行，因此無須開發專屬後台規格。

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
| 多幣別支援 (Multi-Currency) | ✓ (付費功能) | `no11_currency_rate_list_screen.md` + `no12_currency_rate_editor_sreen.md` | ✅ 完整 |
| 解除限制 (Unlimited Access) | ✓ (付費功能) | `no16_paywall_screen.md` + 各編輯器邏輯 | ✅ 完整 |

### 資料與同步 (Data & Sync)

| User Story | 產品定義 | 模組規格對應 | 狀態 |
|-----------|--------|------------|------|
| 離線支援 (Offline Architecture) | ✓ | `no1_module_architecture/no1_architecture_overview.md` (Local-First) | ✅ 完整 |
| 雲端同步引擎 (Sync Engine) | ✓ (付費功能) | `no3_background_logics/no3_batch_sync_spec.md` | ✅ 完整 |
| 資料匯入 (CSV Import) | ✓ (付費功能) | `no15_import_screen.md` | ✅ 完整 |

### 儀表板與體驗 (Dashboard & Experience)

| User Story | 產品定義 | 模組規格對應 | 狀態 |
|-----------|--------|------------|------|
| 首頁儀表板 (Home Dashboard) | ✓ | `no2_home_screen.md` | ✅ 完整 |
| 搜尋功能 (Local Search) | ✓ | `no14_search_screen.md` | ✅ 完整 |
| 多語言支援 (i18n) | ✓ | `no13_preference_screen.md` + `no1_user_management/no3_apis/update_preferences_api.md` | ✅ 完整 |
| 配色主題系統 (Theme System) | ✓ | `no3_background_logics/no5_theme_management.md` + `no5_design_system/no1_theme_tokens.md` | ✅ 完整 |
| 主題切換介面 (Theme Switcher) | ✓ | `no2_screens/no18_theme_settings_screen.md` | ✅ 完整 |
| 新增配色主題 (New Theme) | ✓ | `no5_design_system/no2_built_in_themes.md` | ✅ 完整 |
| 序號驗證系統 (Redeem System) | ✓ | `iap_subscription_flow.md` (架構) + `no1_user_management` | ✅ 完整 |
| 序號兌換介面 (Redeem UI) | ✓ | `no2_screens/no17_redeem_code_screen.md` | ✅ 完整 |
| 序號管理工具 (Redeem Management) | ✓ | (使用 Firebase Console) | ✅ MVP 策略 |

---

## 詳細分析結果

### 1. 核心功能與資產管理
Accounting App 的核心記帳功能（CRUD、帳戶、類別）在規格文件中已有非常詳盡的定義，包含 UI 佈局、互動邏輯與資料流。付費功能（多幣別、定期交易）的權限檢查邏輯也已整合在各個畫面規格中。

### 2. 主題系統 (Theme System)
**狀態：完整覆蓋**
- **設計層面**：`no1_theme_tokens.md` 定義了完整的設計代幣系統。
- **邏輯層面**：`no5_theme_management.md` 規範了主題的初始化、切換與持久化邏輯。
- **UI 層面**：`no18_theme_settings_screen.md` 提供了使用者切換主題的介面規格。

### 3. 序號與會員系統 (Redeem & Membership)
**狀態：完整覆蓋 (MVP 策略)**
- **使用者端**：`no17_redeem_code_screen.md` 定義了序號輸入與兌換的流程。
- **後端邏輯**：`iap_subscription_flow.md` 確立了以 RevenueCat 為核心的混合權限架構。
- **營運端**：針對「序號管理工具」User Story，專案已決定在 MVP 階段直接使用 Firebase Console 進行手動管理，因此不需要開發專屬的管理後台規格。這符合精實開發原則。

### 4. 結論
經過重新檢視，**Accounting App 模組目前不存在規格缺失**。所有產品定義中的 User Stories 都已轉化為具體的規格文件或明確的執行策略。開發團隊可依據現有規格進行實作。


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

### 優先級 1: 補充缺失規格 (已完成)

#### 主題系統
已新增以下文件：
- `no3_module_specs/no2_accounting_app/no2_screens/no18_theme_settings_screen.md`
- `no3_module_specs/no2_accounting_app/no3_background_logics/no5_theme_management.md`
- `no3_module_specs/no2_accounting_app/no5_design_system/no1_theme_tokens.md`

#### 序號兌換系統
已新增以下文件：
- `no3_module_specs/no2_accounting_app/no2_screens/no17_redeem_code_screen.md`
- 架構定義於 `iap_subscription_flow.md`

### 優先級 2: 保持一致性

#### 同步產品定義與模組規格
- 當產品定義修改時，應同步更新對應的模組規格
- 當新增 User Story 時，應規劃對應的模組規格文件

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
