# Users Collection Schema

## Schema 定義

### 基本資料

資料來源：Firebase Auth

| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `uid` | String | ✓ | Firebase Auth UID，與 Document ID 相同 |
| `email` | String | ✓ | 使用者 Email |
| `displayName` | String | - | 顯示名稱，來自 Google 帳號 |
| `photoURL` | String | - | 大頭照 URL，來自 Google 帳號 |
| `provider` | String | ✓ | 認證提供者，MVP 固定為 `google.com` |

---

### 使用者偏好設定

| 欄位 | 型別 | 必填 | 預設值 | 說明 |
|------|------|------|--------|------|
| `preferences.language` | String | ✓ | `'zh-TW'` | 介面語言：`zh-TW`, `en` |
| `preferences.currency` | String | ✓ | `'TWD'` | 主要貨幣 ISO 4217 code |
| `preferences.timezone` | String | ✓ | `'Asia/Taipei'` | 時區 IANA timezone |
| `preferences.theme` | String | - | `'system'` | 主題：`light`, `dark`, `system` |

---

### 訂閱狀態

此區塊由 `verifyIAPReceipt` Cloud Function 在伺服器端驗證收據後寫入，客戶端只讀不寫。使用者尚未購買時，`subscription` 欄位不存在，客戶端應視同 Tier 0。

| 欄位 | 型別 | 說明 |
|------|------|------|
| `subscription.tier` | Number | 訂閱等級，對應 PlanTier 枚舉值，Tier 0 為免費，Tier 1 為 Premium |
| `subscription.expiresAt` | Number | 訂閱到期的毫秒時間戳，終身授權時為 null |
| `subscription.productId` | String | 購買的 Product ID |
| `subscription.platform` | String | 購買平台，值為 ios 或 android |
| `subscription.verifiedAt` | Number | 最後一次伺服器驗證通過的毫秒時間戳 |
| `subscription.environment` | String | 驗證環境，值為 production 或 sandbox |

#### 權限映射 Tier Mapping

| Tier | 判斷條件 | 功能權限 |
| :--- | :--- | :--- |
| **Tier 0 Free** | `subscription` 欄位不存在，或 `expiresAt` 不為 null 且已過期 | 僅本地資料庫，無雲端同步 |
| **Tier 1 Premium** | `subscription.tier` 為 1，且 `expiresAt` 為 null 或未過期 | 啟用 Sync Engine，支援雲端備份與跨裝置同步 |

**範例資料**：
```json
{
  "subscription": {
    "tier": 1,
    "expiresAt": 1767225599000,
    "productId": "susugigi_level1_yearly",
    "platform": "ios",
    "verifiedAt": 1735689600000,
    "environment": "production"
  }
}
```

---

### 系統時間戳

| 欄位 | 型別 | 必填 | 說明 |
|------|------|------|------|
| `createdAt` | Timestamp | ✓ | 使用者首次建立時間 |
| `updatedAt` | Timestamp | ✓ | 最後更新時間 |

---

## 完整範例文件

```json
{
  "uid": "firebase_uid_abc123",
  "email": "ken@example.com",
  "displayName": "Ken Chio",
  "photoURL": "https://lh3.googleusercontent.com/...",
  "provider": "google.com",
  
  "preferences": {
    "language": "zh-TW",
    "currency": "TWD",
    "timezone": "Asia/Taipei",
    "theme": "dark"
  },
  
  "subscription": {
    "tier": 1,
    "expiresAt": 1767225599000,
    "productId": "susugigi_level1_yearly",
    "platform": "ios",
    "verifiedAt": 1735689600000,
    "environment": "production"
  },

  "createdAt": "2025-01-01T08:00:00Z",
  "updatedAt": "2025-01-15T14:30:00Z"
}
```

---

## 權限檢查範例

### App 端檢查是否為 Premium 會員

```typescript
function isPremiumUser(subscription?: Subscription): boolean {
  if (!subscription) return false;
  if (subscription.expiresAt === null) return true;
  return subscription.expiresAt > Date.now();
}
```

### 監聽權限變更

```typescript
useEffect(() => {
  const unsubscribe = firestore()
    .collection('users')
    .doc(currentUser.uid)
    .onSnapshot(doc => {
      const userData = doc.data();
      const subscription = userData?.subscription;
      const tier = isPremiumUser(subscription) ? subscription.tier : PlanTier.LEVEL_0;
      setCurrentTier(tier);
    });

  return () => unsubscribe();
}, [currentUser.uid]);
```

---

## Firestore Security Rules

使用者只能讀取與更新自己的文件。更新時僅允許修改 `preferences` 與 `updatedAt` 欄位，`subscription` 欄位由 Cloud Function 獨佔寫入，客戶端無寫入權限。

```
match /users/{userId} {
  allow read: if request.auth != null && request.auth.uid == userId;
  allow create: if request.auth != null && request.auth.uid == userId;
  allow update: if request.auth != null
                && request.auth.uid == userId
                && request.resource.data.diff(resource.data).affectedKeys()
                   .hasOnly(['preferences', 'updatedAt']);
}
```

---

## 索引建議

**單欄位索引:**
- `email`：用於查詢，但通常直接用 UID 查詢

**複合索引:**
- 無需複合索引，MVP 階段

---

## 注意事項

### ✅ 應該做的
- 透過 Firestore SDK 讀寫使用者偏好
- 監聽 `subscription` 欄位變更以更新 UI 的訂閱狀態
- 使用 `updatedAt` 追蹤資料變更時間

### ❌ 不應該做的
- 客戶端直接寫入 `subscription` 欄位，此欄位僅由 Cloud Function 寫入
- 在 Firestore 中儲存原始收據或任何付款敏感資訊
- 在客戶端自行判斷收據有效性，繞過伺服器驗證流程