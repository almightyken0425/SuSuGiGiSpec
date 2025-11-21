# 使用者層級與生命週期管理待辦事項 (User Tier & Lifecycle Management Todo)

## 1. 資料模型補齊 (Data Model Completion)
**目標**: 在 `no3_module_specs/no1_user_management/no4_data_models/no1_data_models.md` 中補齊 `Users` 表格定義。

- [ ] **定義 `Users` 核心欄位**:
  - `currentTier`: Number (目前會員等級, 0=Free, 1=Premium, etc.)
  - `subscriptionStatus`: String (e.g., 'active', 'expired', 'lifetime')
  - `subscriptionEndDate`: Number (Unix Timestamp, 會員到期日)
  - `nextBillingDate`: Number (若有自動扣款)
  - `autoRenew`: Boolean (是否自動續約)

## 2. 會員狀態更新機制 (Status Update Mechanism)
**問題**: 會員資格有時效性，過期後如何降級？
**方案分析**:
- **Option A: 排程掃描 (Scheduled Job)**
  - 使用 Cloud Scheduler + Cloud Function 每日執行。
  - 優點: 資料庫狀態永遠保持最新，利於後台分析。
  - 缺點: 用戶量大時成本較高。
- **Option B: 觸發式檢查 (Lazy Check / Middleware)**
  - 用戶開啟 App 或呼叫 API 時檢查 `subscriptionEndDate`。
  - 若 `Now > EndDate` 且 `currentTier > 0`，即時觸發降級邏輯。
  - 優點: 節省資源，僅處理活躍用戶。
  - 缺點: 不活躍用戶的資料庫狀態可能過時。

- [ ] **決定策略**: 建議採用 **混合模式 (Hybrid)**。
  - 主要依賴 **App/API 觸發** 確保用戶體驗與權限正確。
  - 輔以 **每日排程** 清理過期很久的帳號狀態 (Data Consistency)。

## 3. 序號兌換與既有資格衝突處理 (Conflict Resolution)
**問題**: 用戶已有會員資格時，兌換新序號該如何處理？

- [ ] **情境 1: 同級展期 (Extension)**
  - 條件: `Current Tier == Target Tier`
  - 邏輯: `New EndDate = Old EndDate + Duration`
- [ ] **情境 2: 升級 (Upgrade)**
  - 條件: `Current Tier < Target Tier`
  - 邏輯: 
    - 方案 A: 直接覆蓋，原剩餘時間失效 (簡單)。
    - 方案 B: 原剩餘時間依比例轉換為新 Tier 時間 (複雜)。
    - 建議 MVP 採方案 A 或方案 B (依商業決策)。
- [ ] **情境 3: 降級/低階序號 (Downgrade)**
  - 條件: `Current Tier > Target Tier`
  - 邏輯: 通常禁止兌換，或存為「待用券」(Voucher) 待目前會籍結束後使用。

## 4. 執行計畫
- [ ] 更新 `no1_data_models.md`
- [ ] 撰寫 `no3_logics/no3_membership_lifecycle.md` (定義上述邏輯)
- [ ] 更新 `no3_logics/no2_redeem_code_validation.md` (加入衝突處理邏輯)
