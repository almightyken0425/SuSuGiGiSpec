# Premium 邏輯規格: PremiumLogic

## 目的

集中管理所有 Premium 權限檢查與同步邏輯，確保離線支援與邏輯一致性。

---

## 核心方法

### checkPremiumStatus

- **簽章:** `checkPremiumStatus(context: PremiumContext): Boolean`
- **性質:** **純本地計算 Local Computation**
- **邏輯:**
    - 檢查 `context.expirationDate`。
    - **IF** `expirationDate` is `Null`:
        - **Return:** `True` 代表 Lifetime Access
    - **IF** `expirationDate` > `Date.now()`:
        - **Return:** `True` 代表 Active Subscription
    - **ELSE:**
        - **Return:** `False` 代表 Expired

### refreshPremiumStatus

- **簽章:** `refreshPremiumStatus(): Promise<void>`
- **性質:** **網路請求 Network Request**
    - 非同步執行。
    - 需處理網路錯誤。
- **邏輯:**
    - 呼叫 `RevenueCat.getCustomerInfo`。
    - 取得最新 `CustomerInfo`。
    - 解析 `entitlements.active['premium']`。
    - **更新本地 PremiumContext:**
        - `rawCustomerInfo` = 最新 JSON。
        - `lastChecked` = `Date.now()`。
        - `expirationDate` = 解析出的到期日，若無則為 Null。
    - **觸發:** UI 重繪，若狀態改變。
