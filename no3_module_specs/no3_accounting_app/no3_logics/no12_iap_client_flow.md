# IAP 客戶端流程規格

## 目的

定義客戶端在購買與恢復購買流程中的完整行為，包含與 `verifyIAPReceipt` Cloud Function 的互動時機，以及訂閱狀態更新的接收方式。

---

## 新購買流程

- 使用者在 PaywallScreen 選擇方案並確認購買
- 呼叫 `iapService.requestPurchase`，帶入選擇的 Product ID
- App Store 或 Google Play 彈出系統購買對話框
- 使用者完成購買後，`iapService` 內部的 `purchaseUpdatedListener` 收到購買事件
- `purchaseUpdatedListener` 取得原始收據後呼叫 `verifyIAPReceipt` Cloud Function，傳入 receipt、productId 與 platform
- **IF Cloud Function 驗證成功:**
    - 呼叫 `finishTransaction` 告知 App Store 或 Google Play 購買已確認
    - Cloud Function 將 `subscription` 寫入 Firestore
    - `PremiumContext` 的 `initSubscriptionListener` 偵測到 `subscription` 更新，自動刷新 `currentTier`
- **IF Cloud Function 驗證失敗:**
    - 不呼叫 `finishTransaction`，保留交易待下次重試
    - 通知 UI 顯示錯誤提示

---

## 恢復購買流程

- 使用者在 PaywallScreen 點擊 `恢復購買`
- 呼叫 `iapService.restorePurchases`，取得裝置上的既有購買紀錄
- 對每筆購買紀錄逐一呼叫 `verifyIAPReceipt` Cloud Function 驗證
- Cloud Function 驗證成功後寫入 Firestore
- `initSubscriptionListener` 偵測到更新，自動刷新 `currentTier`
- **IF 所有購買紀錄均驗證失敗或無購買紀錄:**
    - 通知 UI 顯示找不到購買紀錄

---

## 訂閱狀態監聽

`PremiumContext` 不主動查詢訂閱狀態，改為透過 Firestore 監聽被動接收更新。

- 使用者登入後，呼叫 `PremiumLogic.initSubscriptionListener` 建立 `onSnapshot` 監聽
- 每次 Firestore `subscription` 欄位有變動，`checkPremiumStatus` 自動計算新的 `currentTier`
- 使用者登出時，呼叫 `PremiumLogic.stopSubscriptionListener` 清除監聽器

---

## 開發環境限制

`setMockTier` 僅在 `__DEV__` 旗標為 true 時可用，供開發期間模擬不同訂閱狀態，正式 build 不得於 `PremiumContext` 介面中暴露此方法。
