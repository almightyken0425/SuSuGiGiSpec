# IAP 收據驗證 Cloud Function 規格

## 目的

在伺服器端驗證 IAP 購買收據，確保訂閱狀態由 Apple 或 Google 官方 API 背書後才寫入 Firestore，客戶端無法自行偽造或繞過此流程。

---

## 函式規格

### verifyIAPReceipt

- **類型:** HTTPS Callable Function
- **身份驗證:** 必須攜帶有效的 Firebase Auth Token，未登入請求一律拒絕
- **必要參數:**
    - `receipt` — iOS 為 base64 encoded receipt data，Android 為 purchase token
    - `productId` — 購買的 Product ID，用於對照 tier 映射表
    - `platform` — 購買平台，值為 ios 或 android

---

## 執行邏輯

- 從 Firebase Auth Context 取得呼叫者的 `uid`，確保寫入目標為呼叫者本人的文件
- **IF platform 為 ios:**
    - 向 Apple App Store Server API 發送收據驗證請求
    - 解析回應中的訂閱到期時間 `expires_date_ms` 與訂閱狀態
    - **IF 正式環境收到 sandbox 收據:**
        - 拒絕請求，回傳錯誤狀態 `sandbox-receipt-in-production`
- **IF platform 為 android:**
    - 向 Google Play Developer API 發送訂閱狀態查詢
    - 解析回應中的訂閱到期時間 `expiryTimeMillis` 與訂閱狀態
- **IF 驗證通過:**
    - 依 `productId` 對照 entitlements 設定，解析對應的 `tier` 值
    - 執行 Firestore 寫入，見 Firestore 寫入行為段落
    - 回傳成功
- **IF 驗證失敗:**
    - 不修改 Firestore
    - 回傳明確的錯誤狀態，例如 `invalid-receipt`、`expired-subscription`、`bundle-id-mismatch`

---

## Firestore 寫入行為

驗證通過後，以 `merge: true` 方式寫入 `users/{uid}` 文件的 `subscription` 欄位，不覆蓋其他欄位。

- `subscription.tier` — 依 productId 解析的 PlanTier 枚舉值
- `subscription.expiresAt` — 解析自 Apple 或 Google 回應的到期毫秒時間戳
- `subscription.productId` — 傳入的 productId
- `subscription.platform` — 傳入的 platform
- `subscription.verifiedAt` — `Date.now()` 寫入時的伺服器時間戳
- `subscription.environment` — 依驗證環境設為 production 或 sandbox

---

## 安全性約束

- 正式環境拒絕 sandbox 收據，防止測試收據被認定為有效訂閱
- 驗證 Apple 回應中的 `bundle_id` 或 Google 回應中的 `packageName` 須與應用程式一致，防止跨應用攻擊
- Cloud Function 以服務帳戶身份寫入 Firestore，客戶端的 Firestore Rules 應禁止直接寫入 `subscription` 欄位

---

## Firestore 安全規則要求

`users/{uid}` 文件中，`subscription` 欄位的寫入權限僅限 Cloud Function 服務帳戶，客戶端規則範例如下：

```javascript
match /users/{uid} {
  allow read: if request.auth.uid == uid;
  allow write: if request.auth.uid == uid
    && !request.resource.data.keys().hasAny(['subscription']);
}
```
