# 更新使用者偏好設定 (Update Preferences)

> **實作方式**: 直接使用 Firestore SDK（**不需要** Cloud Function）  
> **原因**: 偏好設定更新是簡單的寫入操作，不涉及複雜邏輯

---

## 為什麼不需要 API？

MVP 階段的偏好設定更新**不需要獨立的 Cloud Function API**，原因：

1. ✅ **簡單操作**: 只是更新 Firestore 文件
2. ✅ **權限控制**: Firestore Security Rules 已足夠
3. ✅ **即時性**: 直接操作比 API 更快
4. ✅ **離線支援**: Firestore SDK 支援離線快取

---

## Firestore Security Rules

確保使用者只能更新自己的偏好設定：

```javascript
// firestore.rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    
    // Users collection
    match /users/{userId} {
      // 使用者可讀取自己的資料
      allow read: if request.auth != null && request.auth.uid == userId;
      
      // 使用者可更新自己的偏好設定（但不能改其他欄位）
      allow update: if request.auth != null 
                    && request.auth.uid == userId
                    && request.resource.data.diff(resource.data).affectedKeys()
                       .hasOnly(['preferences', 'updatedAt']);
      
      // 首次建立由 App 處理（first_login_flow）
      allow create: if request.auth != null && request.auth.uid == userId;
    }
  }
}
```

---

## App 端實作

### 更新單一偏好設定

```typescript
import firestore from '@react-native-firebase/firestore';

/**
 * 更新使用者語言偏好
 */
async function updateLanguagePreference(userId: string, language: string) {
  await firestore()
    .collection('users')
    .doc(userId)
    .update({
      'preferences.language': language,
      updatedAt: firestore.FieldValue.serverTimestamp()
    });
  
  console.log(`Language updated to ${language}`);
}

/**
 * 更新使用者貨幣偏好
 */
async function updateCurrencyPreference(userId: string, currency: string) {
  await firestore()
    .collection('users')
    .doc(userId)
    .update({
      'preferences.currency': currency,
      updatedAt: firestore.FieldValue.serverTimestamp()
    });
  
  console.log(`Currency updated to ${currency}`);
}
```

---

### 批次更新多個偏好

```typescript
/**
 * 一次更新多個偏好設定
 */
async function updateMultiplePreferences(
  userId: string,
  preferences: Partial<UserPreferences>
) {
  const updates: any = {
    updatedAt: firestore.FieldValue.serverTimestamp()
  };
  
  // 動態組合更新欄位
  if (preferences.language) {
    updates['preferences.language'] = preferences.language;
  }
  if (preferences.currency) {
    updates['preferences.currency'] = preferences.currency;
  }
  if (preferences.timezone) {
    updates['preferences.timezone'] = preferences.timezone;
  }
  if (preferences.theme) {
    updates['preferences.theme'] = preferences.theme;
  }
  
  await firestore()
    .collection('users')
    .doc(userId)
    .update(updates);
  
  console.log('Preferences updated:', preferences);
}
```

---

## UI 整合範例

### 設定畫面

```typescript
// PreferenceScreen.tsx
import React, { useState, useEffect } from 'react';
import firestore from '@react-native-firebase/firestore';
import auth from '@react-native-firebase/auth';

function PreferenceScreen() {
  const [language, setLanguage] = useState('zh-TW');
  const [currency, setCurrency] = useState('TWD');
  const [loading, setLoading] = useState(false);
  
  const userId = auth().currentUser?.uid;
  
  // 載入目前偏好
  useEffect(() => {
    if (!userId) return;
    
    const unsubscribe = firestore()
      .collection('users')
      .doc(userId)
      .onSnapshot(doc => {
        const data = doc.data();
        if (data?.preferences) {
          setLanguage(data.preferences.language);
          setCurrency(data.preferences.currency);
        }
      });
    
    return () => unsubscribe();
  }, [userId]);
  
  // 更新語言
  const handleLanguageChange = async (newLanguage: string) => {
    if (!userId) return;
    
    setLoading(true);
    try {
      await firestore()
        .collection('users')
        .doc(userId)
        .update({
          'preferences.language': newLanguage,
          updatedAt: firestore.FieldValue.serverTimestamp()
        });
      
      // 更新 i18n
      i18n.changeLanguage(newLanguage);
      
      showSuccessToast('語言已更新');
    } catch (error) {
      console.error('Failed to update language', error);
      showErrorToast('更新失敗，請稍後再試');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <View>
      <LanguagePicker 
        value={language}
        onChange={handleLanguageChange}
        disabled={loading}
      />
      <CurrencyPicker 
        value={currency}
        onChange={(newCurrency) => {
          // 類似的處理邏輯
        }}
        disabled={loading}
      />
    </View>
  );
}
```

---

## 錯誤處理

### 網路錯誤

```typescript
try {
  await updateLanguagePreference(userId, 'en');
} catch (error) {
  if (error.code === 'firestore/unavailable') {
    // 網路問題，稍後重試
    showWarningToast('網路不穩定，更新將在恢復連線後完成');
  } else if (error.code === 'firestore/permission-denied') {
    // 權限錯誤（不應發生，除非 Security Rules 有問題）
    showErrorToast('權限錯誤');
  } else {
    showErrorToast('更新失敗');
  }
}
```

### 離線模式

Firestore SDK 自動處理離線模式：
- 更新會先寫入本地快取
- 恢復網路後自動同步至伺服器
- 不需要額外處理

---

## 驗證與限制

### 前端驗證

```typescript
function validateLanguage(language: string): boolean {
  const supportedLanguages = ['zh-TW', 'en'];
  return supportedLanguages.includes(language);
}

function validateCurrency(currency: string): boolean {
  // ISO 4217 currency codes
  const supportedCurrencies = ['TWD', 'USD', 'JPY', 'EUR'];
  return supportedCurrencies.includes(currency);
}

// 使用範例
if (!validateLanguage(newLanguage)) {
  showErrorToast('不支援的語言');
  return;
}

await updateLanguagePreference(userId, newLanguage);
```

---

## 監聽即時更新

```typescript
// 監聽偏好設定變更
useEffect(() => {
  const unsubscribe = firestore()
    .collection('users')
    .doc(userId)
    .onSnapshot(
      doc => {
        const data = doc.data();
        if (data?.preferences) {
          // 自動更新 UI
          setLanguage(data.preferences.language);
          setCurrency(data.preferences.currency);
          
          // 更新 i18n
          i18n.changeLanguage(data.preferences.language);
        }
      },
      error => {
        console.error('Failed to listen to user changes', error);
      }
    );
  
  return () => unsubscribe();
}, [userId]);
```

---

## 測試場景

### 場景 1: 線上更新
1. 使用者在設定頁面切換語言
2. Firestore 即時更新
3. UI 立即反映變更

### 場景 2: 離線更新
1. 使用者在無網路環境切換語言
2. 更新寫入本地快取
3. UI 立即反映變更
4. 恢復網路後同步至伺服器

### 場景 3: 多裝置同步
1. 使用者在裝置 A 更新語言
2. Firestore 同步至伺服器
3. 裝置 B 的 `onSnapshot` 監聽器觸發
4. 裝置 B 的 UI 自動更新

---

## 總結

### ✅ 使用 Firestore SDK 的優點
- 無需額外開發 Cloud Function
- 自動離線支援
- 即時同步
- 跨裝置一致

### ⚠️ 何時需要 Cloud Function？
如果未來有以下需求，才考慮加入 API：
- 複雜驗證邏輯
- 需要觸發其他系統操作
- 需要審計日誌
- 需要資料轉換

**MVP 階段不需要**。

---

**文件結束**
