# 產品定義與會計應用規格比較分析

## 執行摘要

本文件比較 [`no1_product_initiation/no2_product_definition.md`](../../no1_product_initiation/no2_product_definition.md) 中定義的 Accounting App User Stories 與 [`no3_module_specs`](../../no3_module_specs) 中的實際規格文件。

### 關鍵發現 (2025-11-24 更新)

- ✅ **核心功能完整覆蓋**：CRUD、資料同步、儀表板等均已具備詳細規格。
- ✅ **主題系統已定義**：新增了設計系統與代幣定義，並在使用者偏好中支援主題切換。
- ✅ **會員與序號架構已確立**：採用 RevenueCat 統一管理架構，序號功能雖延後至 MVP 後，但架構與整合方式已在分析報告中明確定義。
- 📊 **規格深度足夠**：模組規格提供了比產品定義更精細的 UI/UX 和互動邏輯。

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
| 解除限制 (Unlimited Access) | ✓ (付費功能) | 散布於多個畫面的權限檢查邏輯 (參考 `iap_subscription_flow.md`) | ✅ 完整 |

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
| 多語言支援 (i18n) | ✓ | `no1_user_management/no3_apis/update_preferences_api.md` (語系設定) | ✅ 完整 |
| 配色主題系統 (Theme System) | ✓ | `no2_accounting_app/no5_design_system/` + `update_preferences_api.md` | ✅ 完整 |

### 會員與序號系統 (Membership & Redeem)

| User Story | 產品定義 | 模組規格對應 | 狀態 |
|-----------|--------|------------|------|
| 會員權限管理 (Tier System) | ✓ | `iap_subscription_flow.md` + `no1_user_management/no1_data_models/users_schema.md` | ✅ 完整 |
| 序號兌換 (Redeem System) | ✓ | `iap_subscription_flow.md` (定義架構) + `no1_user_management/README.md` (定義範圍) | ⏸️ 延後 (MVP後) |

---

## 詳細分析更新

### 1. 主題系統 (Theme System) - ✅ 已解決

**現況**：
- **設計代幣**：已在 `no2_accounting_app/no5_design_system/no1_design_tokens.md` 中完整定義。
- **資料模型**：`users_schema.md` 中已包含 `preferences.theme` 欄位。
- **切換邏輯**：`update_preferences_api.md` 已定義如何透過 Firestore SDK 更新主題設定。

### 2. 序號兌換系統 (Redeem System) - ⏸️ 架構已定，實作延後

**現況**：
- **架構決策**：採用 RevenueCat 統一管理架構，序號系統簡化為 Cloud Function + RevenueCat API。
- **規格狀態**：
  - `iap_subscription_flow.md` 詳細定義了 IAP 與序號的混合架構與資料流。
  - `no1_user_management/README.md` 明確將序號功能列為 MVP 之後的迭代項目。
  - 舊有的複雜序號規格已歸檔，避免混淆。

### 3. 會員權限管理 (Tier System) - ✅ 已解決

**現況**：
- **權限來源**：由 RevenueCat 統一管理 (`rc_entitlements`)。
- **資料同步**：透過 RevenueCat Firebase Integration 自動寫入 Firestore `users/{uid}`。
- **App 端檢查**：App 僅需監聽 Firestore 文件即可判斷權限，無需複雜的本地邏輯。

---

## 結論

目前的規格文件已經與產品定義高度一致。原先缺失的「主題系統」與「序號系統」已經透過新增規格文件或明確的架構決策補齊。

- **MVP 範圍明確**：User Management 模組已精簡為 MVP 版本。
- **技術架構清晰**：RevenueCat 整合方案解決了複雜的會員與序號管理問題。
- **設計系統就位**：Design Tokens 為主題系統打下基礎。

建議持續保持此狀態，隨時更新規格以反映實作細節的變更。


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
