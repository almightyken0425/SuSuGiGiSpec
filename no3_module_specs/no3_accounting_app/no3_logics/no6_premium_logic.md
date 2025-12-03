# Premium 邏輯規格: PremiumLogic

## 目的

集中管理所有 Premium 權限檢查與同步邏輯，確保離線支援與邏輯一致性。

---

## 核心方法

### checkPremiumStatus

- **簽章:** `checkPremiumStatus(context: PremiumContext): Boolean`
- **性質:** **純本地計算 Local Computation**
    - **絕不** 觸發網路請求。
    - **絕不** 阻塞 UI 渲染。
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

---

## 觸發時機

### refreshPremiumStatus 呼叫點

- **App 啟動 Bootstrap:**
    - 在背景執行同步，不阻擋 UI。
- **登入成功 Post-Auth:**
    - 確保取得該帳號的最新權限。
- **購買成功 Paywall:**
    - 立即更新權限狀態。
- **恢復購買成功 Paywall:**
    - 立即更新權限狀態。

### checkPremiumStatus 呼叫點

- **所有權限檢查點:**
    - 畫面進入前檢查，例如 Settings 或 Feature Entry。
    - 功能執行前檢查，例如 Import 或 Sync。
    - 背景排程檢查，例如 Batch Sync。
