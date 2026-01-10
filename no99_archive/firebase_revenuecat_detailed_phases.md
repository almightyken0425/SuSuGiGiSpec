# Firebase & RevenueCat 串接施工計劃 - 詳細子階段

> **文件日期:** 2026-01-03  
> **最後更新:** 2026-01-06  
> **版本:** v2.1 執行中版本  
> **母文件:** `firebase_revenuecat_integration_plan_20260103.md`  
> **執行狀態:** ✅ 階段0完成 | ✅ 階段2完成 | ✅ 階段3完成 | ✅ 階段4完成 | 🚀 階段5(測試)準備中

---

## 階段拆解總覽

1.  **階段 0: 準備工作 (Preparation)**
    - 0.1: React Native Version Evaluation
    - 0.2: Developer Accounts
    - 0.3: Product Planning
2.  **階段 1: RevenueCat 基礎整合 (Foundation)**
    - 1.1: Dashboard Setup
    - 1.2: Service Implementation
    - 1.3: Paywall UI
    - 1.4: Sandbox Testing
3.  **階段 2: Firebase Auth 整合 (Authentication)**
    - 2.1: Project Setup (iOS/Android)
    - 2.2: SDK Integration
    - 2.3: iOS Config
    - 2.4: Android Config
    - 2.5: Service Implementation
    - 2.6: UI Integration
    - 2.7: Integration Testing
4.  **階段 3: Firestore 資料同步 (Data Sync)**
    - 3.1: Firestore Setup
    - 3.2: Users Collection
    - 3.3: RevenueCat Extension
    - 3.4: Preference Sync
    - 3.5: SyncEngine Foundation
    - 3.6: Premium Logic
5.  **階段 4: 完整同步引擎 (Full Engine)**
    - 4.1: Collection Design
    - 4.2: Incremental Sync
    - 4.3: Initial Sync
    - 4.4: Error Handling
    - 4.5: UI Integration
6.  **階段 5: 整合測試與優化 (Optimization)**
    - 5.1: E2E Testing
    - 5.2: Performance
    - 5.3: Monitoring
    - 5.4: Documentation

---

## ✅ 階段 0: 準備工作 (已完成)

### ✅ 子階段 0.1: React Native 版本評估 (已完成)

**預估時間:** 0.5 天

**原定工作內容:**
- 檢查當前專案狀態與版本資訊
- 研究 RN 0.79.6 breaking changes
- 檢查套件相容性
- 建立版本評估報告

**產出:**
- 版本評估報告 `version_evaluation_report.md`

**實際執行紀錄 (Actual Execution):**
- **Evaluation:** 評估了從 RN 0.83.x 降級至 0.79.6 的必要性，主要為了配合 Firebase Native SDK 的穩定性。
- **Decision:** 決定降級以確保與 `@react-native-firebase` 生態系的完全相容。

---

### ✅ 子階段 0.2: Firebase 與 RevenueCat 免費帳號準備 (已完成)

**預估時間:** 0.5 天

**原定工作內容:**
- 規劃 Firebase 專案建立步驟
- 規劃 RevenueCat 免費帳號註冊
- 建立帳號準備檢查清單

**產出:**
- 帳號準備清單 `developer_accounts_checklist.md`

**實際執行紀錄 (Actual Execution):**
- **Accounts:** 完成 Firebase Project 建立與 RevenueCat 帳號註冊。
- **Setup:** 建立了基礎的開發環境配置。

---

### ✅ 子階段 0.3: RevenueCat 產品規劃 (已完成)

**預估時間:** 0.5 天

**原定工作內容:**
- 定義訂閱產品結構 (月費、年費)
- 規劃定價策略
- 設計 Entitlement 架構
- 建立產品規格文件

**產出:**
- 產品規格書 `revenuecat_product_spec.md`

**實際執行紀錄 (Actual Execution):**
- **Products:** 確定了 `pro_monthly` 與 `pro_yearly` 兩大訂閱產品。
- **Entitlements:** 定義 `premium` level entitlement，並將其與 Firestore user schema 中的 `rc_entitlements` 欄位對齊。

## ✅ 階段 1: RevenueCat 基礎整合 (架構已完成)

### ✅ 子階段 1.1: RevenueCat Dashboard 設定 (已完成)

**預估時間:** 0.5 天

**原定工作內容:**
- 建立 RevenueCat 專案
- 連結 Apple App Store
- 連結 Google Play Store
- 建立月訂閱產品
- 建立年訂閱產品
- 設定免費試用期間
- 建立 Entitlement: premium
- 取得 API Keys

**產出:**
- RevenueCat 專案設定截圖
- API Keys 文件
- 產品 ID 列表

**實際執行紀錄 (Actual Execution):**
- **Dashboard:** 已建立專案與 Entitlements。
- **Keys:** 已取得 Public API Keys 並配置於專案常數中 (待填入真實值)。
- **Products:** 定義了 `pro_monthly` 與 `pro_yearly` 標識符。

---

### ✅ 子階段 1.2: RevenueCat 服務層實作 (已完成)

**預估時間:** 1 天

**原定工作內容:**
- 更新 `revenueCat.ts`
- 移除 Mock 模式
- 實作 `getOfferings`
- 實作 `purchasePackage`
- 實作 `restorePurchases`
- 實作錯誤處理
- 實作離線邏輯
- 更新 `PremiumContext.tsx`
- 加入 `expirationDate` 追蹤
- 實作 `checkPremiumStatus`
- 實作離線 TTL 檢查

**產出:**
- 更新的 `revenueCat.ts`
- 更新的 `PremiumContext.tsx`
- 單元測試

**實際執行紀錄 (Actual Execution):**
- **Service:** `revenueCat.ts` 已整合 `react-native-purchases` SDK。
- **Context:** `PremiumContext` 已實作 `CustomerInfo` 監聽與狀態管理。
- **Schema:** 確保 `entitlements` 資料結構與 Firestore 同步需求一致。

---

### ✅ 子階段 1.3: PaywallScreen UI 實作 (已完成)

**預估時間:** 1 天

**原定工作內容:**
- 更新 `PaywallScreen.tsx`
- 串接 `getOfferings` API
- 動態顯示價格
- 實作購買按鈕
- 實作恢復購買按鈕
- 實作 Loading 狀態
- 實作錯誤提示
- 實作 Redirect Flow

**產出:**
- 更新的 `PaywallScreen.tsx`
- UI 測試案例

**實際執行紀錄 (Actual Execution):**
- **UI:** Paywall 介面已完成，包含 Restore 與 Purchase 按鈕。
- **Mock Integration:** 在真實 Key 上線前，支援透過 `setIsMockMode` 進行 UI 測試。

---

### 子階段 1.4: RevenueCat 沙盒測試 (部分完成)

**預估時間:** 1 天

**原定工作內容:**
- 建立 iOS TestFlight build
- 建立 Android Internal Testing build
- 測試沙盒購買
- 測試恢復購買
- 測試訂閱過期
- 測試離線權限檢查
- 記錄測試結果

**產出:**
- 測試報告
- 問題清單
- 修復計劃

**實際執行紀錄 (Actual Execution):**
- **Pending:** 等待最終 App Store Connect 設定與 TestFlight 部署驗證。目前主要透過 Mock Mode 驗證流程。

---

## ✅ 階段 2: Firebase Auth 整合 (已完成)

### ✅ 子階段 2.1: Firebase 專案設定 (已完成)

**預估時間:** 0.5 天

**原定工作內容:**
- 建立 Firebase 專案
- 啟用 Authentication
- 設定 Google OAuth
- 註冊 iOS App
- 註冊 Android App
- 下載設定檔案
- 設定 OAuth 同意畫面

**產出:**
- Firebase 專案 URL
- `GoogleService-Info.plist`
- `google-services.json`
- OAuth Client IDs

**實際執行紀錄 (Actual Execution):**
- **Configuration:** 完成 Firebase Console 設定。
- **Files:** 下載並配置 `GoogleService-Info.plist` (iOS) 與 `google-services.json` (Android)。

---

### ✅ 子階段 2.2: React Native 降級與 SDK 安裝 (已完成 - 含 Firestore 修復)

**預估時間:** 0.5 天

**原定工作內容:**
- 執行 RN 降級至 0.79.6
- 安裝 `@react-native-firebase/app@21.14.0`
- 安裝 `@react-native-firebase/auth@21.14.0`
- 安裝 `@react-native-firebase/firestore@21.14.0` (務必鎖定版本避免 v23.0.0+ 衝突)
- 安裝 `@react-native-google-signin/google-signin`
- 執行 `npm install`
- 測試 build

**產出:**
- 更新的 `package.json`
- 成功解決 leveldb-library 編譯衝突 (使用 `CLANG_ALLOW_NON_MODULAR_INCLUDES_IN_FRAMEWORK_MODULES`)

**實際執行紀錄 (Actual Execution):**
- **Downgrade:** 成功將 RN 版本從 0.83.x 降級至 0.79.6 以解決 Native Module 相容性問題。
- **Dependencies:** 鎖定 `@react-native-firebase/*` 版本於 v19.x/v21.x (視最終 lock檔)，並安裝 Google Sign-In。
- **Build Fix:** 解決了 Ruby 版本與 CocoaPods 相容性問題。

---

### ✅ 子階段 2.3: iOS 專案配置 (已完成)

**預估時間:** 1 天

**原定工作內容:**
- 複製 `GoogleService-Info.plist` 至專案
- 更新 `Podfile`
- 加入 static frameworks 清單
- 設定 pre_install hook
- 加入 `CLANG_ALLOW_NON_MODULAR_INCLUDES_IN_FRAMEWORK_MODULES = 'YES'`
- 明確宣告 Firebase pods
- 更新 `AppDelegate.swift`
- 匯入 Firebase modules
- 呼叫 `FirebaseApp.configure()`
- 設定 URL Schemes
- 執行 `pod install`
- 測試 iOS build

**產出:**
- 更新的 `Podfile`
- 更新的 `AppDelegate.swift`
- iOS build 成功

**實際執行紀錄 (Actual Execution):**
- **Podfile:** 實作 `static_frameworks` hook 強制將 Firebase 庫編譯為靜態框架，解決 `use_frameworks!` 衝突。
- **AppDelegate:** 完成 `FirebaseApp.configure()` 初始化。

---

### ✅ 子階段 2.4: Android 專案配置 (已完成)

**預估時間:** 0.5 天

**原定工作內容:**
- 複製 `google-services.json` 至 `android/app/`
- 更新 `android/build.gradle`
- 加入 Google Services plugin
- 更新 `android/app/build.gradle`
- 套用 plugin
- 設定 SHA-1 憑證
- 測試 Android build

**產出:**
- 更新的 Gradle 設定檔
- Android build 成功

**實際執行紀錄 (Actual Execution):**
- **Gradle:** 更新 Project 與 App level `build.gradle` 加入 Google Services Classpath 與 Plugin。

---

### ✅ 子階段 2.5: Firebase Auth 服務層實作 (已完成)

**預估時間:** 1 天

**原定工作內容:**
- 更新 `firebase.ts`
- 移除 Mock 實作
- 實作 Firebase Auth 初始化
- 實作 `signInWithGoogle`
- 實作 `signOut`
- 實作 `onAuthStateChanged`
- 整合 Google Sign-In SDK
- 實作 Token 轉換
- 實作錯誤處理

**產出:**
- 更新的 `firebase.ts`
- Auth 服務單元測試

**實際執行紀錄 (Actual Execution):**
- **Implementation:** `firebase.ts` 完整實作 `signInWithGoogle`，包含 `GoogleSignin.signIn()` 取得 idToken 並轉換為 `auth.GoogleAuthProvider.credential`。
- **Error Handling:** 加入 `try-catch` 與錯誤碼對應。

---

### ✅ 子階段 2.6: AuthContext 與 LoginScreen 實作 (已完成)

**預估時間:** 1 天

**原定工作內容:**
- 更新 `AuthContext.tsx`
- 連接 Firebase Auth
- 實作 `onAuthStateChanged` 訂閱
- 同步至 WatermelonDB
- 整合 RevenueCat identify
- 實作重試機制
- 更新 `LoginScreen.tsx`
- 建立 Google 登入按鈕
- 實作錯誤提示
- 實作 Loading 狀態
- 實作 Redirect Flow

**產出:**
- 更新的 `AuthContext.tsx`
- 更新的 `LoginScreen.tsx`
- UI 測試案例

**實際執行紀錄 (Actual Execution):**
- **Context:** `AuthContext` 監聽 Firebase Auth 狀態，並維護 `user` 與 `isLoading` 狀態。
- **UI:** `LoginScreen` 整合 Google Sign-In 按鈕，並處理登入後的導航邏輯 (跳轉至 Home 或 Settings)。
- **Sync Trigger:** 登入成功後自動觸發 `syncUserToFirestore`。

---

### ✅ 子階段 2.7: Firebase Auth 整合測試 (已完成)

**預估時間:** 1 天

**原定工作內容:**
- 測試 Google 登入流程
- 測試登出流程
- 測試網路錯誤處理
- 測試使用者資料同步
- 測試 RevenueCat 識別
- 測試跨裝置登入
- 記錄測試結果

**產出:**
- 測試報告
- 問題清單
- 修復計劃

**實際執行紀錄 (Actual Execution):**
- **Verification:** 透過 iOS Simulator Logs 確認 `[Auth] Sign in success` 與 Token 獲取成功。
- **Flow:** 驗證從 Login -> Google Auth -> Firebase Auth -> App Home 的完整流程。

## ✅ 階段 3: Firestore 資料同步 (已完成)

### ✅ 子階段 3.1: Firestore 基礎設定 (已完成)

**預估時間:** 0.5 天

**原定工作內容:**
- 啟用 Firestore Database
- 選擇資料庫區域
- 建立 Security Rules
- 設定 users collection 規則
- 建立基本索引
- 測試 Rules

**產出:**
- Firestore Security Rules 檔案
- 索引設定文件

**實際執行紀錄 (Actual Execution):**
- **Firestore Console:** 已啟用 Native Mode，區域設定完成。
- **Security Rules:** 建立 `firestore.rules`，設定 `match /users/{userId}` 僅限本人讀寫 (`request.auth.uid == userId`)。
- **規則測試:** 透過 `permission-denied` 錯誤驗證了規則的有效性 (當 User ID 不匹配時拒絕寫入)。

---

### ✅ 子階段 3.2: Users Collection 實作 (已完成)

**預估時間:** 1 天

**原定工作內容:**
- 實作使用者建立邏輯
- 實作重試機制
- 實作 Schema 驗證
- 實作偏好設定欄位
- 測試使用者建立
- 測試查詢效能

**產出:**
- Users Collection 實作程式碼
- Schema 驗證規則

**實際執行紀錄 (Actual Execution):**
- **UserService:** 實作 `userService.ts`，包含 `syncUserToFirestore` 與 `updateUserPreferences`。
- **AuthContext:** 在登入成功後自動觸發 `syncUserToFirestore`。
- **Schema Alignment:** 確保 `FirestoreUser` 介面包含 `email`, `displayName`, `photoUrl`, `providers` 等欄位。

---

### ✅ 子階段 3.3: RevenueCat Firebase Extension 整合 (已完成)

**預估時間:** 0.5 天

**原定工作內容:**
- 安裝 RevenueCat Extension
- 設定 API Key
- 配置 Webhook
- 設定目標 Collection
- 測試權限同步
- 測試過期處理

**產出:**
- Extension 設定文件
- Webhook 測試報告

**實際執行紀錄 (Actual Execution):**
- **Schema Update:** 更新 `coreSchema.ts` 加入 `rc_entitlements` 與 `rc_active_subscriptions` 欄位，以配合 Extension 的輸出格式。
- **Field Removal:** 從 App 端移除 `isPremium` 寫入邏輯，避免與 Extension 的權限來源衝突。
- **Local DB:** 更新 WatermelonDB `users` table 加入對應的 JSON 欄位以支援離線存取。

---

### ✅ 子階段 3.4: 偏好設定同步實作 (已完成)

**預估時間:** 1 天

**原定工作內容:**
- 實作本地寫入 Firestore
- 實作 Firestore Listener
- 實作衝突解決
- 實作 PreferenceContext 整合
- 測試跨裝置同步
- 測試離線處理

**產出:**
- 偏好同步程式碼
- 同步測試案例

**實際執行紀錄 (Actual Execution):**
- **Service:** 實作 `settingsService.ts` 處理 `user_settings` 的同步。
- **Context:** `PreferenceContext` 整合了 `updateUserPreferences`，變更語言/幣別/主題時自動寫入 Firestore。

---

### ✅ 子階段 3.5: SyncEngine 基礎框架 (已完成)

**預估時間:** 1 天

**原定工作內容:**
- 建立 `syncEngine.ts`
- 實作 `start` 方法
- 實作 `stop` 方法
- 實作連線狀態檢查
- 實作 timestamp 比對
- 實作基礎上傳框架
- 實作基礎下載框架

**產出:**
- `syncEngine.ts` 檔案
- SyncEngine 架構文件

**實際執行紀錄 (Actual Execution):**
- **Core Class:** 建立 `SyncEngine` class，實作 `pullChanges` 與 `pushChanges` 核心方法。
- **Type Safety:** 定義泛型介面 `SyncableModel` 確保所有同步模型具備 `id`, `updated_on`, `is_deleted`。
- **Collections:** 預先支援 `Accounts`, `Categories`, `Transactions`, `Transfers` 等主要資料表。

---

### ✅ 子階段 3.6: Premium 升降級邏輯 (已完成)

**預估時間:** 1 天

**原定工作內容:**
- 實作升級觸發邏輯
- 實作 Initial Sync 觸發
- 實作降級觸發邏輯
- 實作 Sync 停止邏輯
- 實作狀態通知
- 測試升級流程
- 測試降級流程

**產出:**
- 升降級邏輯程式碼
- 升降級測試報告

**實際執行紀錄 (Actual Execution):**
- **Trigger:** 在 `PremiumContext` 中監聽權限變更。
- **Force Sync:** 在 `SettingsScreen` 實作 "Force Sync Now" 按鈕，手動觸發 `syncEngine.sync()`。
- **User Repair:** 在 Force Sync 流程中加入 `syncUserToFirestore` 修復邏輯，解決手動刪庫後 User Profile 遺失的問題。

## ✅ 階段 4: 完整同步引擎 (已完成)

### ✅ 子階段 4.1: Firestore Collections Schema 設計 (已完成)

**預估時間:** 1 天

**原定工作內容:**
- 設計 transactions schema
- 設計 accounts schema
- 設計 categories schema
- 設計 recurring_settings schema
- 設計索引策略
- 建立 Security Rules
- 測試 Rules

**產出:**
- Schema 設計文件
- Security Rules 更新
- 索引設定文件

**實際執行紀錄 (Actual Execution):**
- **Schema Design:** 完整定義了 `accounts`, `categories`, `transactions`, `transfers`, `currency_rates`, `schedules` 六大 Collections 的 Schema。
- **Fields:** 加入必要欄位 `id`, `updated_on`, `is_deleted` 以支援增量同步與軟刪除。
- **Mappers:** 實作 Local (Snake Case) <-> Remote (Camel Case) 的自動轉換 Mapper。

---

### ✅ 子階段 4.2: 增量同步實作 (已完成)

**預估時間:** 2 天

**原定工作內容:**
- 實作上傳查詢邏輯
- 實作批次寫入
- 實作下載查詢邏輯
- 實作批次更新
- 實作 timestamp 更新
- 實作 LWW 衝突解決
- 測試增量同步

**產出:**
- 增量同步程式碼
- 同步測試案例

**實際執行紀錄 (Actual Execution):**
- **Pull Logic:** 實作 `pullChanges(lastSyncedAt)`，僅拉取 `updatedOn > lastSyncedAt` 的資料。
- **Push Logic:** 實作 `pushChanges`，上傳本地標記為 Dirty 的資料。
- **Conflict Resolution:** 採用 Last Write Wins (LWW) 策略，若 Remote 時間戳較新則覆蓋本地。
- **Soft Delete:** 支援刪除同步 (syncing `isDeleted: true`)。

---

### ✅ 子階段 4.3: Initial Sync 實作 (已完成)

**預估時間:** 2 天

**原定工作內容:**
- 實作觸發邏輯判斷
- 實作完整上傳邏輯
- 實作完整下載邏輯
- 實作合併邏輯
- 實作批次處理
- 實作進度追蹤
- 測試 Initial Sync

**產出:**
- Initial Sync 程式碼
- 進度追蹤 UI

**實際執行紀錄 (Actual Execution):**
- **Unified Logic:** Initial Sync 與增量同步共用同一套 `sync()` 邏輯，當 `lastSyncedAt` 為 0 時自動判定為 Initial Sync，執行全量拉取。
- **Batching:** 實作分批處理 (Batch Size: 500)，避免 Firestore Quota 或記憶體溢位。

---

### ✅ 子階段 4.4: 錯誤處理與重試 (已完成)

**預估時間:** 1 天

**原定工作內容:**
- 實作網路錯誤處理
- 實作重試機制
- 實作指數退避
- 實作 Quota 錯誤處理
- 實作錯誤記錄
- 測試錯誤情境

**產出:**
- 錯誤處理程式碼
- 錯誤情境測試報告

**實際執行紀錄 (Actual Execution):**
- **Error Handling:** 核心 `sync()` 流程包覆在 `try-catch` 中。
- **Recovery:** 實作 `resetSyncState` 用於發生嚴重錯誤時重置時間戳，強制如下次執行完整同步。
- **Logging:** 整合詳細的 console logs 方便除錯。

---

### ✅ 子階段 4.5: SyncContext 與 UI 整合 (已完成)

**預估時間:** 1 天

**原定工作內容:**
- 建立 `SyncContext.tsx`
- 實作狀態管理
- 更新 SettingsScreen
- 加入同步狀態顯示
- 加入手動同步按鈕
- 加入上次同步時間
- 測試 UI 互動

**產出:**
- `SyncContext.tsx` 檔案
- 更新的 SettingsScreen
- UI 測試案例

**實際執行紀錄 (Actual Execution):**
- **UI Integration:** 整合於 `SettingsScreen`，提供 "Force Sync Now" 按鈕。
- **Developer Tools:** 加入 "Reset Database" 功能方便測試。
- **User Repair:** 針對 Force Sync 加入了自動修復 User Profile 的邏輯 (Sync Permission Fix)。

---

## 階段 5: 整合測試與優化

### 子階段 5.1: 端到端測試

**預估時間:** 2 天

**工作內容:**
- 執行情境 1: 新使用者流程
- 執行情境 2: 升級流程
- 執行情境 3: 過期處理
- 執行情境 4: 恢復購買
- 執行情境 5: 離線使用
- 記錄測試結果
- 修復發現問題

**產出:**
- E2E 測試報告
- 問題與修復清單

**驗收標準:**
- 所有情境通過
- 無重大問題
- 使用者體驗良好

---

### 子階段 5.2: 效能優化

**預估時間:** 1 天

**工作內容:**
- 分析 Firestore 讀寫次數
- 實作智慧同步頻率
- 優化 WatermelonDB 查詢
- 優化 App 啟動時間
- 實作延遲載入
- 測試效能改善

**產出:**
- 效能優化報告
- 優化程式碼

**驗收標準:**
- Firestore 讀寫降低 30%
- App 啟動時間 < 3 秒
- 同步效能提升

---

### 子階段 5.3: 成本監控與錯誤追蹤

**預估時間:** 1 天

**工作內容:**
- 整合 Firebase Crashlytics
- 設定錯誤追蹤
- 建立成本監控儀表板
- 設定 Firestore 預算警報
- 設定 RevenueCat 監控
- 建立關鍵指標追蹤

**產出:**
- Crashlytics 設定
- 成本監控儀表板
- 指標追蹤報告

**驗收標準:**
- Crashlytics 正常運作
- 成本監控準確
- 指標可視化

---

### 子階段 5.4: 文件更新與審查

**預估時間:** 1 天

**工作內容:**
- 更新 README
- 建立環境設定指南
- 建立故障排除文件
- 補充程式碼註解
- 建立 API 文件
- 審查 Security Rules
- 執行 Rules 測試

**產出:**
- 完整文件集
- Security Rules 審查報告

**驗收標準:**
- 文件完整清晰
- Security Rules 無漏洞
- 新成員可依文件上手

---

## 時程規劃建議

### 超快速路徑: 2 週

**適合:** 全職開發，已有 Firebase 經驗

- **週 1:** 階段 0 + 階段 1 + 階段 2.1~2.4
- **週 2:** 階段 2.5~2.7 + 階段 3 + 階段 4 + 階段 5

### 快速路徑: 4 週

**適合:** 全職開發，邊學邊做

- **週 1:** 階段 0 + 階段 1
- **週 2:** 階段 2
- **週 3:** 階段 3 + 階段 4.1
- **週 4:** 階段 4.2~4.5 + 階段 5

### 穩健路徑: 6 週

**適合:** 兼職開發，充分測試

- **週 1-2:** 階段 0 + 階段 1
- **週 3:** 階段 2.1~2.4
- **週 4:** 階段 2.5~2.7 + 階段 3.1~3.3
- **週 5:** 階段 3.4~3.6 + 階段 4
- **週 6:** 階段 5

### 謹慎路徑: 8 週

**適合:** 業餘時間開發，品質優先

- **週 1:** 階段 0
- **週 2:** 階段 1
- **週 3:** 階段 2.1~2.4
- **週 4:** 階段 2.5~2.7
- **週 5:** 階段 3.1~3.3
- **週 6:** 階段 3.4~3.6
- **週 7:** 階段 4
- **週 8:** 階段 5

---

## 階段依賴關係

### 必須依序執行

- 0.1 → 0.2 → 0.3
- 1.1 → 1.2 → 1.3 → 1.4
- 2.1 → 2.2 → 2.3 & 2.4 → 2.5 → 2.6 → 2.7
- 3.1 → 3.2 → 3.3 & 3.4 → 3.5 → 3.6
- 4.1 → 4.2 & 4.3 → 4.4 → 4.5
- 5.1 → 5.2 → 5.3 → 5.4

### 可平行執行

- 2.3 與 2.4 可同時進行
- 3.3 與 3.4 可同時進行
- 4.2 與 4.3 可同時進行
- 5.2 與 5.3 可同時進行

---

## 檢查清單模板

每個子階段完成後填寫：

```markdown
## 子階段 X.Y 完成檢查

- [ ] 所有工作項目已完成
- [ ] 產出文件已建立
- [ ] 驗收標準全部通過
- [ ] 程式碼已提交 Git
- [ ] 團隊已審查
- [ ] 可進入下一子階段
```

---

**文件結束**
