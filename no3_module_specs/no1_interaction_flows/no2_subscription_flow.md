# 訂閱流程總覽

## 目的

描述訂閱相關事件在各模組與元件之間的完整流動路徑，包含購買、到期、恢復購買與狀態同步，作為各模組規格的跨模組索引。

---

## 模組職責分界

訂閱機制橫跨兩個模組，各自有明確邊界。

**User Management 模組負責:**
- Firestore `users/{uid}.subscription` 欄位的 schema 定義
- `verifyIAPReceipt` Cloud Function，唯一有權寫入 `subscription` 欄位的元件
- Apple App Store Server API 與 Google Play Developer API 的溝通

**Accounting App 模組負責:**
- `iapService`，封裝 react-native-iap，處理系統購買對話框與收據取得
- `PremiumContext`，維護 App 內的 `currentTier` 狀態，監聽 Firestore 變化
- `PaywallScreen`，購買與恢復購買的 UI 入口
- `SyncEngine`，依 `currentTier` 決定是否啟動雲端同步

---

## 正向訂閱流程

使用者從 PaywallScreen 發起購買至訂閱生效的完整鏈路。

- `PaywallScreen` 載入時呼叫 `iapService.getSubscriptions`，從 App Store 或 Google Play 取得本地化價格顯示
- 使用者選擇方案，`PaywallScreen` 呼叫 `iapService.requestPurchase`
- App Store 或 Google Play 彈出系統購買對話框，使用者完成付款
- `iapService` 的 `purchaseUpdatedListener` 收到購買事件，取得原始收據
- `iapService` 呼叫 `verifyIAPReceipt` Cloud Function，傳入收據、productId 與 platform
- Cloud Function 向 Apple 或 Google 官方 API 驗證收據，確認訂閱有效
- 驗證通過後，Cloud Function 將 `subscription` 寫入 Firestore `users/{uid}`
- `iapService` 呼叫 `finishTransaction`，告知 App Store 或 Google Play 購買已確認
- `PremiumContext` 的 `initSubscriptionListener` 透過 `onSnapshot` 偵測到 `subscription` 更新
- `checkPremiumStatus` 計算出 `currentTier` 升至 `PlanTier.LEVEL_1`
- `SyncEngine` 啟動，執行首次完整同步將本地資料備份至雲端
- `PaywallScreen` 偵測到 `currentTier` 變更，顯示升級成功並關閉

---

## 訂閱到期流程

使用者在 App Store 或 Google Play 取消訂閱，不在 App 內操作，App 端的感知方式如下。

- 取消訂閱後，既有的訂閱週期仍有效至 `subscription.expiresAt`
- App 每次啟動時，`initSubscriptionListener` 讀取 Firestore `subscription` 欄位
- `checkPremiumStatus` 比對 `expiresAt` 與當前時間
- **IF `expiresAt` 已過期:**
    - `currentTier` 降至 `PlanTier.LEVEL_0`
    - `SyncEngine` 停止，本地資料保留，雲端資料凍結
    - 付費功能入口顯示為鎖定狀態

訂閱到期的偵測完全依賴 `expiresAt` 的本地比對，不需要額外的網路請求。Firestore SDK 的離線快取確保 App 在無網路環境下也能正確判斷。

---

## 恢復購買流程

使用者換裝置或重新安裝 App 後，需恢復既有訂閱。

- 使用者在 `PaywallScreen` 點擊恢復購買
- `iapService.restorePurchases` 向裝置查詢既有購買紀錄
- 對每筆購買紀錄逐一呼叫 `verifyIAPReceipt` Cloud Function 驗證
- Cloud Function 驗證成功後更新 Firestore `subscription`
- `initSubscriptionListener` 偵測到更新，`currentTier` 刷新
- **IF 無有效購買紀錄:**
    - `currentTier` 維持 `PlanTier.LEVEL_0`，顯示找不到購買紀錄

---

## 自動續訂處理

使用者的訂閱到期後由 App Store 或 Google Play 自動續訂時，Firestore 中的 `subscription.expiresAt` 不會自動延長，需透過下列方式更新。

- **App 啟動重新驗證:** App 啟動時主動呼叫 `verifyIAPReceipt`，傳入裝置上最新的購買收據，Cloud Function 重新向 Apple 或 Google 查詢並更新 `expiresAt`
- **伺服器推送通知（進階）:** 設定 Apple App Store Server Notifications 或 Google Play Real-time Developer Notifications，讓 Apple 或 Google 在續訂事件發生時主動呼叫 Cloud Function，自動更新 Firestore，不依賴使用者開啟 App

MVP 階段採用 App 啟動重新驗證，伺服器推送通知為未來優化方向。

---

## 訂閱狀態在模組間的流動示意

```
App Store / Google Play
        │
        │ 購買收據
        ▼
   iapService                        (Accounting App)
        │
        │ receipt + productId + platform
        ▼
verifyIAPReceipt Cloud Function      (User Management)
        │
        │ 驗證通過，寫入 subscription
        ▼
Firestore users/{uid}.subscription   (User Management)
        │
        │ onSnapshot
        ▼
PremiumContext.currentTier           (Accounting App)
        │
        ├──► SyncEngine 啟動或停止   (Accounting App)
        ├──► PaywallScreen 關閉      (Accounting App)
        └──► 付費功能解鎖或鎖定      (Accounting App)
```
