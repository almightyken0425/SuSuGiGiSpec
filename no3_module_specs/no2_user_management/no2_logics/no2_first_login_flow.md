# 首次登入流程

> [!NOTE]
> 完整互動流程圖請參閱: `no1_interaction_flows/no1_user_management_flows.md`

## 實作邏輯

### 使用者登入

React Native App 端使用 Firebase Auth 進行 Google 登入。取得 `idToken` 後建立憑證並登入 Firebase，取得使用者物件。

```typescript
// React Native App 端
import auth from '@react-native-firebase/auth';

async function handleGoogleLogin() {
  try {
    // Google 登入
    const googleUser = await GoogleSignin.signIn();
    const googleCredential = auth.GoogleAuthProvider.credential(
      googleUser.idToken
    );
    
    // Firebase Auth 登入
    const userCredential = await auth().signInWithCredential(googleCredential);
    const user = userCredential.user;
    
    // 檢查並建立使用者文件
    await ensureUserDocument(user);
    
    // 導航至主畫面
    navigation.navigate('Home');
  } catch (error) {
    console.error('Login failed', error);
    showErrorDialog('登入失敗，請稍後再試');
  }
}
```

### 檢查並建立使用者文件

使用 Firestore SDK 檢查 `users` 集合中是否已存在該 UID 的文件。若不存在則建立新文件，並寫入預設偏好設定。

```typescript
import firestore from '@react-native-firebase/firestore';
import { FirebaseAuthTypes } from '@react-native-firebase/auth';

async function ensureUserDocument(user: FirebaseAuthTypes.User) {
  const userRef = firestore().collection('users').doc(user.uid);
  
  // 使用 get() 檢查文件是否存在
  const userDoc = await userRef.get();
  
  if (!userDoc.exists) {
    // 文件不存在，建立新使用者
    console.log('New user detected, creating user document...');
    
    await userRef.set({
      uid: user.uid,
      email: user.email,
      displayName: user.displayName || '',
      photoURL: user.photoURL || '',
      provider: 'google.com',
      
      preferences: {
        language: getDeviceLanguage(), // zh-TW or en
        currency: 'TWD',
        timezone: getDeviceTimezone(), // Asia/Taipei
        theme: 'system'
      },
      
      // RevenueCat 欄位初始為空
      rc_entitlements: {},
      rc_active_subscriptions: [],
      
      createdAt: firestore.FieldValue.serverTimestamp(),
      updatedAt: firestore.FieldValue.serverTimestamp()
    });
    
    console.log('User document created successfully');
  } else {
    // 文件已存在，更新登入時間
    await userRef.update({
      updatedAt: firestore.FieldValue.serverTimestamp()
    });
    
    console.log('Existing user logged in');
  }
}
```

### 輔助函式

用於取得裝置目前的語言與時區設定，作為預設值。

```typescript
/**
 * 取得裝置語言設定
 */
function getDeviceLanguage(): string {
  const deviceLang = NativeModules.I18nManager.localeIdentifier || 'zh-TW';
  
  // 支援的語言列表
  const supportedLanguages = ['zh-TW', 'en'];
  
  // 檢查裝置語言是否支援
  if (supportedLanguages.includes(deviceLang)) {
    return deviceLang;
  }
  
  // 預設值
  return 'zh-TW';
}

/**
 * 取得裝置時區
 */
function getDeviceTimezone(): string {
  return RNLocalize.getTimeZone() || 'Asia/Taipei';
}
```

## 錯誤處理

### 網路錯誤

若遇到 `firestore/unavailable` 錯誤，表示目前無網路連線。在此情況下，App 應採用 Local-First 架構繼續運行，待網路恢復後再同步。

```typescript
try {
  await ensureUserDocument(user);
} catch (error) {
  if (error.code === 'firestore/unavailable') {
    // 網路問題，使用本地快取繼續
    console.warn('Firestore unavailable, using cache');
    // App 可正常運行
  } else {
    // 其他錯誤
    console.error('Failed to create user document', error);
    throw error;
  }
}
```

### 並發問題

如果多個裝置同時首次登入，Firestore 的 `set()` 操作具有冪等性，重複執行不會造成資料錯誤。

## RevenueCat 初始化

在建立使用者文件後，使用 Firebase UID 初始化 RevenueCat SDK。此步驟會觸發 RevenueCat 與 Firebase 的整合同步。

```typescript
import Purchases from 'react-native-purchases';

async function initializeRevenueCat(user: FirebaseAuthTypes.User) {
  // 配置 RevenueCat
  await Purchases.configure({
    apiKey: Platform.OS === 'ios' ? IOS_API_KEY : ANDROID_API_KEY,
    appUserID: user.uid // 關鍵：使用 Firebase UID
  });
  
  console.log('RevenueCat initialized with user:', user.uid);
  
  // 獲取最新訂閱狀態
  const customerInfo = await Purchases.getCustomerInfo();
  console.log('Customer info:', customerInfo);
}
```

## 測試場景

### 場景 1: 全新使用者
1. 使用者首次使用 Google 登入
2. Firestore 建立新文件
3. RevenueCat 建立新 subscriber
4. 文件包含預設偏好設定

### 場景 2: 既有使用者
1. 使用者在新裝置登入
2. Firestore 返回既有文件
3. RevenueCat 恢復訂閱狀態
4. App 顯示既有偏好設定

### 場景 3: 離線首次登入
1. 使用者在無網路環境登入
2. 若發生，延後建立文件至恢復網路時
3. App 使用本地預設值運行

## 注意事項

### ✅ 最佳實踐
- 使用 `serverTimestamp()` 而非客戶端時間
- 確保冪等性
- 優雅處理網路錯誤

### ⚠️ 避免
- 不要在建立文件時執行複雜邏輯
- 不要阻塞 UI
- 不要假設 Firestore 操作一定成功
