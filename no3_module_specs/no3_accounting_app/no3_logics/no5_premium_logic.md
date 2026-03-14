# Premium 邏輯規格: PremiumLogic

## 目的

集中管理所有 Premium 權限檢查與同步邏輯，確保離線支援與邏輯一致性。訂閱狀態的真相來源為 Firestore `users/{uid}.subscription`，由 Cloud Function 寫入，本模組只負責讀取與解析。

---

## 核心方法

### checkPremiumStatus

- **簽章:** `checkPremiumStatus(subscription?: Subscription): PlanTier`
- **性質:** **純本地計算 Local Computation**
- **邏輯:**
    - **IF** `subscription` 不存在:
        - **Return:** `PlanTier.LEVEL_0`
    - **IF** `subscription.expiresAt` 為 `null`:
        - **Return:** `subscription.tier` 代表終身授權
    - **IF** `subscription.expiresAt` > `Date.now()`:
        - **Return:** `subscription.tier` 代表訂閱有效
    - **ELSE:**
        - **Return:** `PlanTier.LEVEL_0` 代表訂閱已到期

### initSubscriptionListener

- **簽章:** `initSubscriptionListener(uid: string): void`
- **性質:** **Firestore 即時監聽 Realtime Listener**
- **邏輯:**
    - 對 Firestore `users/{uid}` 建立 `onSnapshot` 監聽
    - 每次收到更新時，讀取 `subscription` 欄位
    - 呼叫 `checkPremiumStatus` 解析對應的 `PlanTier`
    - 更新本地 `currentTier` 狀態，觸發 UI 重繪
    - **IF** 讀取失敗或網路中斷:
        - 保留上一次已知的 `currentTier`，不強制降級

### stopSubscriptionListener

- **簽章:** `stopSubscriptionListener(): void`
- **性質:** **清理 Cleanup**
- **邏輯:**
    - 取消 `onSnapshot` 監聽
    - 重設本地 `currentTier` 為 `PlanTier.LEVEL_0`

---

## 觸發時機

- **initSubscriptionListener:** 使用者登入成功後呼叫
- **stopSubscriptionListener:** 使用者登出時呼叫，或重新登入前先呼叫確保舊監聽器被清除

---

## 開發環境

`setMockTier` 僅在 `__DEV__` 旗標為 true 時可用，用於開發期間模擬不同訂閱狀態，正式 build 不得暴露此方法。
