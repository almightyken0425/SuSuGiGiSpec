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

### RevenueCat 權限資料

> [!IMPORTANT]
> **此區塊由 RevenueCat Firebase Integration 自動寫入，不應手動修改**

| 欄位 | 型別 | 說明 |
|------|------|------|
| `rc_entitlements` | Object | RevenueCat 權限物件，自動同步 |
| `rc_active_subscriptions` | Array | 啟用中的訂閱 Product IDs |

#### 權限映射 Entitlement Mapping

| App Tier | RevenueCat Entitlement ID | 說明 | 功能權限 |
| :--- | :--- | :--- | :--- |
| **Tier 0 Free** | 無 | 免費版使用者 | 僅本地資料庫，無雲端同步 |
| **Tier 1 Premium** | `premium` | 付費訂閱者 | 啟用 Sync Engine，支援雲端備份與跨裝置同步 |

**範例資料**：
```json
{
  "rc_entitlements": {
    "premium": {
      "expires_date": "2025-12-31T23:59:59Z",
      "product_identifier": "com.yourapp.premium.monthly",
      "purchase_date": "2025-01-01T10:00:00Z"
    }
  },
  "rc_active_subscriptions": ["com.yourapp.premium.monthly"]
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
  
  "rc_entitlements": {
    "premium": {
      "expires_date": "2025-12-31T23:59:59Z",
      "product_identifier": "com.yourapp.premium.monthly",
      "purchase_date": "2025-01-01T10:00:00Z"
    }
  },
  "rc_active_subscriptions": ["com.yourapp.premium.monthly"],
  
  "createdAt": "2025-01-01T08:00:00Z",
  "updatedAt": "2025-01-15T14:30:00Z"
}
```

---

## 權限檢查範例

### App 端檢查是否為 Premium 會員

```typescript
function isPremiumUser(user: User): boolean {
  // 直接讀取 RevenueCat 同步的資料
  return user.rc_entitlements?.premium !== undefined;
}
```

### 監聽權限變更

```typescript
// React Native 範例
useEffect(() => {
  const unsubscribe = firestore()
    .collection('users')
    .doc(currentUser.uid)
    .onSnapshot(doc => {
      const userData = doc.data();
      const isPremium = userData.rc_entitlements?.premium !== undefined;
      
      setUserPremiumStatus(isPremium);
    });
  
  return () => unsubscribe();
}, [currentUser.uid]);
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
- 透過 Firestore SDK 直接讀寫使用者偏好
- 監聽 `rc_entitlements` 變更以更新 UI
- 使用 `updatedAt` 追蹤資料變更時間

### ❌ 不應該做的
- **不要手動修改** `rc_entitlements` 或 `rc_active_subscriptions`，由 RevenueCat 管理
- 不要在 Firestore 中儲存敏感資訊，如密碼、信用卡資料
- 不要手動管理訂閱狀態，交給 RevenueCat