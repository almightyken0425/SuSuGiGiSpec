# IAP 訂閱與序號系統完整流程 (Hybrid Subscription Architecture)

> **建立日期**: 2025-11-24  
> **架構模式**: 混合模式 (IAP + 自建序號系統)  
> **核心原則**: RevenueCat 作為權限管理的單一真理來源 (Single Source of Truth)

---

## 系統核心架構

### 設計理念
我們採用 **"Unified Entitlement Source"** 策略：
無論使用者的權限來自 **App Store 購買**、**Google Play 購買** 還是 **序號兌換**，最終都由 **RevenueCat** 統一管理，並透過 **Firebase Integration** 自動同步到 Firestore。

這意味著：
1.  **App** 只需要監聽 Firestore 的 `users/{uid}` 文件，就能知道使用者是否有權限。
2.  **序號系統** 就像是一個「小型的 IAP 供應商」，負責驗證序號並通知 RevenueCat 發放權限。

### 系統角色定義

| 系統 | 角色 | 主要職責 |
|------|------|---------|
| **App** | 客戶端 | 顯示 UI、呼叫 SDK (IAP)、呼叫 Cloud Function (序號)、監聽 Firestore |
| **RevenueCat** | **權限中台** | 統一管理所有來源的權限、處理跨平台同步、自動寫入 Firestore |
| **App Store / GP** | 支付渠道 | 處理金流 (IAP) |
| **Your Backend** | **序號渠道** | 驗證序號有效性、呼叫 RevenueCat API 發放權限 |
| **Firestore** | 狀態儲存 | 被動接收 RevenueCat 的同步資料，供 App 讀取 |

---

### 系統關係圖 (Unified Flow)

```mermaid
graph TB
    subgraph "客戶端"
        App[App]
    end
    
    subgraph "權限來源 (Inputs)"
        Store[App Store / Google Play]
        Serial[序號系統 (Cloud Function)]
    end
    
    subgraph "核心中台 (Hub)"
        RC[RevenueCat Server]
    end
    
    subgraph "狀態儲存 (Output)"
        DB[Firestore]
    end
    
    %% IAP 流程
    App -->|1. 購買| Store
    Store -->|2. 收據| RC
    
    %% 序號流程
    App -->|1. 輸入序號| Serial
    Serial -->|2. 驗證 & Grant API| RC
    
    %% 統一輸出
    RC ==>|3. Auto Sync (Firebase Integration)| DB
    DB -.->|4. 監聽狀態| App
```

---

## 詳細流程說明

### 流程 A: 一般 IAP 購買 (Store Channel)

這是標準的 RevenueCat 流程，完全自動化。

1.  **App**: 使用者點擊購買，呼叫 `Purchases.purchasePackage()`。
2.  **Store**: 處理扣款，回傳收據。
3.  **RevenueCat**: 驗證收據，更新內部狀態。
4.  **Sync**: RevenueCat 透過 Integration 自動更新 Firestore。
5.  **App**: 監聽 Firestore 變更，即時解鎖功能。

### 流程 B: 序號兌換 (Serial Code Channel)

這相當於我們自己建立了一個「小型 IAP」，只是支付方式是「輸入代碼」。

#### 1. 使用者輸入序號
App 呼叫後端 API：
```typescript
// Client Side
const result = await functions().httpsCallable('redeemCode')({ code: 'VIP-2025' });
```

#### 2. 後端驗證與授權 (Cloud Function)
這是最關鍵的一步：**驗證序號 -> 通知 RevenueCat**。

```typescript
// Cloud Function: redeemCode
export const redeemCode = functions.https.onCall(async (data, context) => {
  const userId = context.auth.uid;
  const code = data.code;
  
  // 1. 驗證序號 (您的業務邏輯)
  // 檢查 SerialCodes collection
  const codeDoc = await db.collection('SerialCodes').doc(code).get();
  if (!codeDoc.exists || codeDoc.data().isUsed) {
    throw new functions.https.HttpsError('invalid-argument', '無效或已使用的序號');
  }
  
  // 2. 標記序號為已使用 (避免重複兌換)
  await codeDoc.ref.update({ 
    isUsed: true, 
    usedBy: userId, 
    usedAt: admin.firestore.FieldValue.serverTimestamp() 
  });
  
  // 3. 呼叫 RevenueCat API 發放權限 (Grant Entitlement)
  // 這一步等於告訴 RevenueCat: "這個人付費了(用序號)，請給他權限"
  // POST https://api.revenuecat.com/v1/subscribers/{app_user_id}/entitlements/{entitlement_identifier}/promotional
  await axios.post(`https://api.revenuecat.com/v1/subscribers/${userId}/entitlements/premium/promotional`, {
    duration: 'monthly', // 或 'weekly', 'annual', 'lifetime'
    start_time_ms: Date.now()
  }, {
    headers: { 
      'Authorization': `Bearer ${REVENUECAT_SECRET_KEY}`,
      'Content-Type': 'application/json'
    }
  });
  
  return { success: true };
});
```

#### 3. 狀態同步 (Auto Sync)
當上述 API 呼叫成功後，RevenueCat 會：
1.  在其資料庫中將該使用者標記為 Premium。
2.  **自動觸發 Firebase Integration**。
3.  將最新的權限狀態寫入 Firestore 的 `users/{userId}` (或 `subscribers` 集合)。

#### 4. App 獲得更新
App 不需要處理 API 的回傳結果來更新 UI，而是繼續**監聽 Firestore**。
當 Firestore 被 RevenueCat 更新時，App UI 自動變為 Premium 狀態。

---

## 資料結構 (Firestore)

由 RevenueCat Integration 自動維護的結構範例。
建議將 RevenueCat 的資料寫入 `users/{userId}` 的一個子欄位 (例如 `subscription`) 或是獨立的 `subscribers/{userId}` 文件。

```json
// path: users/{userId}
{
  "displayName": "Ken",
  "email": "ken@example.com",
  
  // RevenueCat 自動寫入的區塊
  "revenueCat": {
    "entitlements": {
      "premium": {
        "expires_date": "2025-12-31T23:59:59Z",
        "grace_period_expires_date": null,
        "product_identifier": "promotional", // 序號來源通常顯示為 promotional
        "purchase_date": "2025-01-01T10:00:00Z"
      }
    },
    "active_subscriptions": [
      "rc_promo_premium_monthly" // 或是 IAP 的 product_id
    ],
    "management_url": null
  }
}
```

---

## 總結：為什麼這樣設計更好？

1.  **單一邏輯 (Single Logic)**：App 前端不需要寫兩套邏輯（一套判斷 IAP，一套判斷序號）。只要 Firestore 裡有權限，就是有權限。
2.  **狀態一致 (Consistency)**：避免了「後端資料庫說他是會員，但 RevenueCat 說他不是」的資料不同步問題。
3.  **簡化維護 (Maintenance)**：序號功能變成了一個單純的「觸發器」，複雜的權限計算（過期時間、續訂狀態）全部交給 RevenueCat 處理。
4.  **擴充性 (Scalability)**：未來如果要加「客服手動贈送」或「邀請碼獎勵」，都只要呼叫同一個 RevenueCat API，前端完全不用改。

---

**文件結束**
