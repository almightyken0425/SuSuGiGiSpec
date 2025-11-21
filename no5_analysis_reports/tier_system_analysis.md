# 付費 Tier 定義與規格對應分析

## 執行摘要

您的觀察**完全正確**。[`no3_business_model.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no1_product_initiation/no3_business_model.md) 定義了完整的 5 層 Tier 系統（Tier 0, 1, 2, 3, B），但 [`no1_accounting_app`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app) 規格文件僅使用簡化的**布林值 `isPremiumUser`**，完全沒有 Tier 數值定義或多層級權限管理機制。

---

## 商業模型定義的 Tier 系統

### 完整 Tier 列表

根據 [`no3_business_model.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no1_product_initiation/no3_business_model.md)：

| Tier | 層級名稱 | 行銷名稱 | 定價 | 所屬模組 | 功能範圍 |
|------|---------|---------|------|---------|---------|
| **Tier 0** | Local | Free | $0 / 月 | Accounting App | 本機記帳、無雲端同步 |
| **Tier 1** | Cloud | Standard | $30 / 月 | Accounting App | + 雲端同步、自動備份、共用帳本 |
| **Tier 2** | Management | Pro | $90 / 月 | **Web Console** | + Web 控制台、進階篩選、客製化報表 |
| **Tier 3** | Intelligence | Ultra | $140 / 月 | **AI Advisor** | + 現金流預測、AI 問答、財務健康診斷 |
| **Tier B** | Enterprise | - | $500+ / 月 | **Macro Data Service** | B2B 數據服務、API |

### 關鍵觀察

1. **Tier 0-1 屬於 Accounting App**：記帳 App 本身的免費與付費版
2. **Tier 2-3 屬於其他模組**：需要額外的 Web Console 和 AI Advisor
3. **Tier B 完全獨立**：B2B 企業服務，與 C 端 Accounting App 無直接關係

---

## Accounting App 規格的實際定義

### 使用的權限機制

在 `no1_accounting_app` 規格中，**僅使用布林值**：

#### 資料模型定義
[`no4_data_models/no1_data_models.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no4_data_models/no1_data_models.md#L243):
```markdown
- `settingKey`: String - Not Null, 例如 baseCurrencyId, timeZone, language, isPremiumUser, lastRecurringCheckDate
```

**問題：**
- ❌ 僅有 `isPremiumUser` (布林值)
- ❌ 沒有 `userTier` 或 `subscriptionTier` 欄位
- ❌ 無法區分 Tier 0 vs Tier 1 vs Tier 2 的細微差異

#### 權限檢查邏輯
所有畫面規格中的權限檢查都是：

```markdown
- **檢查:** `PremiumContext.isPremiumUser`
- **IF** True: 允許存取
- **IF** False: 導航至 PaywallScreen
```

**來源檔案範例：**
- [`no2_home_screen.md#L115`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no2_screens/no2_home_screen.md#L115)
- [`no3_transaction_editor_screen.md#L76`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no2_screens/no3_transaction_editor_screen.md#L76)
- [`no11_currency_rate_list_screen.md#L52`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no2_screens/no11_currency_rate_list_screen.md#L52)

**問題：**
- ❌ 無法支援「Tier 1 可存取、但 Tier 2 才能用進階功能」的邏輯
- ❌ 無法為未來的 Tier 擴展預留空間

#### Paywall 畫面
[`no16_paywall_screen.md`](file:///c:/Users/ken.chio/OneDrive%20-%20%E5%8B%9D%E5%92%8C%E7%A7%91%E6%8A%80%E6%9C%89%E9%99%90%E5%85%AC%E5%8F%B8/%E6%96%87%E4%BB%B6/Repository/SuSuGiGiSpec/no3_module_specs/no1_accounting_app/no2_screens/no16_paywall_screen.md) 定義：

```markdown
- **訂閱選項區:**
    - **選項 - 年度方案**
    - **選項 - 月度方案**
```

**問題：**
- ❌ 僅提供「Premium」升級，未區分 Tier 1 vs Tier 2 vs Tier 3
- ❌ 與商業模型的 5 層 Tier 系統不一致
- ❌ 無法讓使用者選擇要訂閱哪個 Tier

---

## 搜尋結果總結

### 在 `no1_accounting_app` 中的 "Tier" 搜尋結果
```
No results found
```

**結論：** 整個 `no1_accounting_app` 規格文件中**沒有任何提到 Tier 0, 1, 2, 3, B 的地方**。

### 在 `no1_accounting_app` 中的 "premium" 搜尋結果
找到 **20 筆**，全部都是使用 `isPremiumUser` 布林值進行權限檢查。

**結論：** 規格中僅實作了「免費 vs 付費」的二元區分，沒有多層級 Tier 系統。

---

## 差異分析表

| 項目 | 商業模型定義 | Accounting App 規格 | 差異說明 |
|------|------------|-------------------|---------|
| **Tier 總數** | 5 層 (0, 1, 2, 3, B) | 2 層 (免費, Premium) | ⚠️ 規格簡化為布林值 |
| **Tier 欄位** | 應為 0-3 或 B | `isPremiumUser: boolean` | ⚠️ 無數值型 Tier 欄位 |
| **Tier 0 (Free)** | 明確定義 | 對應 `isPremiumUser = false` | ✅ 概念對應 |
| **Tier 1 (Standard)** | 明確定義 ($30/月) | 對應 `isPremiumUser = true` | ⚠️ 與 Tier 2、3 無區別 |
| **Tier 2 (Pro)** | 明確定義 ($90/月) | ❌ 無對應 | ❌ 缺少 |
| **Tier 3 (Ultra)** | 明確定義 ($140/月) | ❌ 無對應 | ❌ 缺少 |
| **Tier B (Enterprise)** | 明確定義 | ❌ 完全不在 Accounting App 範圍 | ✅ 正確，應屬其他模組 |
| **Paywall 選項** | 應提供多 Tier 選擇 | 僅「升級至 Premium」 | ⚠️ 無法選擇 Tier |
| **權限檢查** | 應檢查 `userTier >= requiredTier` | 僅檢查 `isPremiumUser == true` | ⚠️ 無法支援分層權限 |

---

## 規格歸屬問題分析

### 您的問題：這些機制應該歸在哪裡？

#### 選項 A: 放在 `no1_accounting_app` 內
**不適合的原因：**
- ❌ Tier 系統是**跨模組**的（涵蓋 Accounting App, Web Console, AI Advisor）
- ❌ Tier B (Enterprise) 與 Accounting App 無關
- ❌ 使用者的 Tier 等級應該是**全域性**的，不專屬於單一模組

#### 選項 B: 在 `no3_module_specs` 下另建資料夾 ✅ **推薦**

**建議結構：**
```
no3_module_specs/
├── no0_user_management/          # 新建：使用者與權限管理
│   ├── no1_user_model.md         # 使用者資料模型
│   ├── no2_tier_system.md        # Tier 系統定義
│   ├── no3_subscription_logic.md # 訂閱邏輯
│   └── no4_permission_matrix.md  # 權限矩陣
├── no1_accounting_app/
├── no2_web_console/              # 未來建立
├── no3_ai_advisor/               # 未來建立
└── no4_macro_data_service/       # 未來建立
```

**理由：**
- ✅ 使用者管理是**基礎設施**，應獨立於各模組
- ✅ Tier 系統需要**統一定義**，避免各模組重複或衝突
- ✅ 訂閱邏輯（如 RevenueCat 整合）是**共用服務**
- ✅ 權限矩陣需要明確定義「哪個 Tier 可存取哪些功能」

---

## 建議的改善方案

### 優先級 1: 建立使用者管理模組規格

#### 新建 `no3_module_specs/no0_user_management/no1_user_model.md`

建議包含：

```markdown
# 使用者資料模型

## Users 表 (Firestore)

- `userId`: String, Auth UID - Primary Key
- `email`: String
- `displayName`: String
- `currentTier`: Number - 0, 1, 2, 3 或 字串 'B'
- `subscriptionStatus`: String - 'active', 'trial', 'expired', 'cancelled'
- `subscriptionPlatform`: String - 'ios', 'android', 'web', 'manual'
- `subscriptionStartDate`: Number, Unix Timestamp ms
- `subscriptionEndDate`: Number, Unix Timestamp ms
- `createdOn`: Number, Unix Timestamp ms
- `updatedOn`: Number, Unix Timestamp ms

## 本機 Settings 表 (同步自 Users)

- `settingKey: 'userTier'`: String - 值為 '0', '1', '2', '3', 'B'
- `settingKey: 'subscriptionStatus'`: String
```

#### 新建 `no3_module_specs/no0_user_management/no2_tier_system.md`

建議包含：

```markdown
# Tier 系統定義

## Tier 映射表

| Tier | 數值 | 行銷名稱 | 包含模組 |
|------|------|---------|---------|
| Tier 0 | 0 | Free | Accounting App (本機) |
| Tier 1 | 1 | Standard | Accounting App (雲端) |
| Tier 2 | 2 | Pro | Accounting App + Web Console |
| Tier 3 | 3 | Ultra | 全部 C 端模組 + AI |
| Tier B | 'B' | Enterprise | Macro Data Service (B2B) |

## 權限檢查邏輯

### 功能權限映射

- **雲端同步:** `userTier >= 1`
- **共用帳本:** `userTier >= 1`
- **多幣別:** `userTier >= 1`
- **定期交易:** `userTier >= 1`
- **Web Console:** `userTier >= 2`
- **AI Advisor:** `userTier >= 3`
- **Macro API:** `userTier == 'B'`

### 程式碼範例

\`\`\`typescript
function hasFeatureAccess(feature: Feature, userTier: number | 'B'): boolean {
  const featureTierMap = {
    'cloud_sync': 1,
    'shared_ledger': 1,
    'multi_currency': 1,
    'recurring_transaction': 1,
    'web_console': 2,
    'ai_advisor': 3,
  };
  
  if (typeof userTier === 'string') {
    return feature === 'macro_api';
  }
  
  return userTier >= featureTierMap[feature];
}
\`\`\`
```

#### 新建 `no3_module_specs/no0_user_management/no3_subscription_logic.md`

建議包含：

```markdown
# 訂閱邏輯規格

## RevenueCat 配置

### Product IDs

- `tier1_monthly`: Tier 1 月訂閱 ($30)
- `tier1_yearly`: Tier 1 年訂閱 ($300)
- `tier2_monthly`: Tier 2 月訂閱 ($90)
- `tier2_yearly`: Tier 2 年訂閱 ($900)
- `tier3_monthly`: Tier 3 月訂閱 ($140)
- `tier3_yearly`: Tier 3 年訂閱 ($1,400)

### Entitlements

- `tier_1_access`: 解鎖 Tier 1 功能
- `tier_2_access`: 解鎖 Tier 2 功能
- `tier_3_access`: 解鎖 Tier 3 功能

## 購買後同步邏輯

1. RevenueCat webhook 通知
2. 更新 Firestore Users.currentTier
3. 觸發 App 內 Settings 同步
4. 更新 PremiumContext 狀態
```

### 優先級 2: 修改 Accounting App 規格

#### 修改 `no4_data_models/no1_data_models.md`

將：
```markdown
- `settingKey`: String - Not Null, 例如 isPremiumUser
```

改為：
```markdown
- `settingKey`: String - Not Null, 例如 userTier, subscriptionStatus
- `settingValue` 範例:
  - `userTier`: '0', '1', '2', '3', 'B'
  - `subscriptionStatus`: 'active', 'trial', 'expired'
```

#### 修改權限檢查邏輯

將所有畫面規格中的：
```markdown
- **檢查:** `PremiumContext.isPremiumUser`
```

改為：
```markdown
- **檢查:** `PremiumContext.userTier >= requiredTier`
  - **雲端同步:** requires Tier >= 1
  - **定期交易:** requires Tier >= 1
```

#### 修改 `no16_paywall_screen.md`

新增 Tier 選擇邏輯：

```markdown
## UI 佈局

- **Tier 選擇區:** (新增)
    - **UI:** Tab 或 Segmented Control
    - **選項:**
        - **Standard (Tier 1):** $30/月 - 雲端同步與進階記帳
        - **Pro (Tier 2):** $90/月 - 包含 Web 控制台
        - **Ultra (Tier 3):** $140/月 - 包含 AI 財務顧問
    - **預設:** 依使用者需求推薦（例: 若來自 Web Console 頁面，預選 Tier 2）

- **訂閱選項區:** (修改)
    - **基於選中的 Tier** 顯示對應的月度/年度方案
```

### 優先級 3: 建立權限矩陣文件

#### 新建 `no3_module_specs/no0_user_management/no4_permission_matrix.md`

```markdown
# 功能權限矩陣

| 功能 | Tier 0 | Tier 1 | Tier 2 | Tier 3 | Tier B |
|------|--------|--------|--------|--------|--------|
| **Accounting App** |
| 本機記帳 CRUD | ✅ | ✅ | ✅ | ✅ | ❌ |
| 雲端同步 | ❌ | ✅ | ✅ | ✅ | ❌ |
| 共用帳本 | ❌ | ✅ | ✅ | ✅ | ❌ |
| 多幣別 | ❌ | ✅ | ✅ | ✅ | ❌ |
| 定期交易 | ❌ | ✅ | ✅ | ✅ | ❌ |
| 無限帳戶/類別 | ❌ | ✅ | ✅ | ✅ | ❌ |
| 資料匯入 | ❌ | ✅ | ✅ | ✅ | ❌ |
| **Web Console** |
| 桌面表格視圖 | ❌ | ❌ | ✅ | ✅ | ❌ |
| JQL 查詢 | ❌ | ❌ | ✅ | ✅ | ❌ |
| 客製化報表 | ❌ | ❌ | ✅ | ✅ | ❌ |
| **AI Advisor** |
| 現金流預測 | ❌ | ❌ | ❌ | ✅ | ❌ |
| AI 問答 | ❌ | ❌ | ❌ | ✅ | ❌ |
| 財務健康診斷 | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Macro Data Service** |
| 市場情資儀表板 | ❌ | ❌ | ❌ | ❌ | ✅ |
| 總經 API | ❌ | ❌ | ❌ | ❌ | ✅ |
```

---

## 總結與建議

### 您的觀察驗證 ✅

1. **商業模型定義了 Tier 0-3 和 Tier B** ✅ 正確
2. **Tier B 不應包含在 Accounting App 規格中** ✅ 正確，它屬於獨立的 B2B 服務
3. **當前規格僅使用布林值 `isPremiumUser`** ✅ 正確，缺少 Tier 數值定義
4. **規格應該定義 Premium 欄位並填入 0, 1, 2** ✅ 正確方向，但應定義為 `userTier`

### 關鍵建議 🎯

> [!IMPORTANT]
> **核心建議：在 `no3_module_specs` 下建立 `no0_user_management` 資料夾**
> 
> 使用者權限與 Tier 系統是**跨模組的基礎設施**，不應綁定在單一模組（如 Accounting App）內。建立獨立的 User Management 規格可以：
> - 統一管理 Tier 定義
> - 避免各模組重複或衝突
> - 為未來的 Web Console、AI Advisor 模組預留清晰的權限接口

### 行動步驟

**Phase 1: 建立基礎架構規格（當前優先）**
1. 建立 `no3_module_specs/no0_user_management/` 資料夾
2. 撰寫 `no1_user_model.md`（使用者資料模型，包含 `currentTier` 欄位）
3. 撰寫 `no2_tier_system.md`（Tier 0-3, B 的完整定義與權限邏輯）
4. 撰寫 `no4_permission_matrix.md`（功能權限矩陣）

**Phase 2: 修改 Accounting App 規格**
1. 修改 `no1_data_models.md`，將 `isPremiumUser` 改為 `userTier`
2. 修改所有畫面規格的權限檢查邏輯（從布林值改為 Tier 比較）
3. 修改 `no16_paywall_screen.md`，支援多 Tier 選擇

**Phase 3: 補充訂閱邏輯**
1. 撰寫 `no3_subscription_logic.md`（RevenueCat 配置與同步邏輯）
2. 定義 Tier 升級/降級的用戶流程

### 與商業模型的一致性檢查

修改後的規格應滿足：
- ✅ 清晰區分 Tier 0 (免費) vs Tier 1 (付費基礎)
- ✅ 預留 Tier 2、3 的擴展空間（即使 Accounting App 不直接使用）
- ✅ Tier B 獨立於 C 端系統，不混淆
- ✅ 所有功能都能明確映射到所需的最低 Tier

---

**您的分析非常準確！** 當前規格確實缺少完整的 Tier 系統定義，建議按照上述方案在 `no3_module_specs/no0_user_management` 下建立專門的使用者權限管理規格。
