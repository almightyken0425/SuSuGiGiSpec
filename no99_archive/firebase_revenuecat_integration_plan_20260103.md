# Firebase & RevenueCat 串接施工計劃

> **文件日期:** 2026-01-03  
> **專案:** SuSuGiGi 記帳 App  
> **目標:** 實作使用者認證、付費訂閱與雲端同步功能

---

## 當前狀態總結

### 已完成項目

- WatermelonDB 本地資料庫已建立
- RevenueCat SDK 已安裝版本 9.6.12
- PremiumContext 骨架已建立
- AuthContext 骨架已建立
- PaywallScreen UI 已實作

### Mock 狀態

- Firebase 服務: 目前為 Mock 模式
- RevenueCat 服務: 目前為 Mock 模式
- 所有權限檢查皆為假資料

### 技術風險與解決方案

> [!IMPORTANT]
> **已驗證解決方案:** 根據實際成功案例，Firebase Native SDK 可在 React Native 0.79.6 正常運作。

**iOS 整合問題:**
- React Native 0.83.1 與 Native Firebase SDK 有已知相容性問題
- **驗證解決方案:** 降級至 React Native 0.79.6 可完美整合
- **參考案例:** 已成功整合 `@react-native-firebase/app` v23.4.0 與 `@react-native-firebase/messaging` v23.4.0
- **關鍵配置:** 需使用 static frameworks 配置，詳見參考 Podfile

**Android 整合:**
- 無已知相容性問題
- 可完整使用 Native SDK

---

## 階段 0: 環境準備與風險評估

### 目標

確認技術可行性並制定最終技術選型策略。

### 工作項目

- **React Native 版本評估**
    - **當前版本:** React Native 0.83.1
    - **建議版本:** React Native 0.79.6
    - **決策考量:**
        - 降級至 0.79.6 可使用 Native Firebase SDK
        - Native SDK 效能優於 Web SDK
        - 已有成功整合案例可參考
    - **影響評估:**
        - 檢查現有程式碼是否相容 0.79.6
        - 評估降級風險與收益
        - 確認第三方套件相容性
- **Firebase SDK 選型決策**
    - **推薦方案:** Native SDK `@react-native-firebase/app`
    - **條件:** 若同意降級至 RN 0.79.6
    - **備用方案:** Firebase Web SDK 若必須保持 RN 0.83.1
- **RevenueCat 產品規劃**
    - 確認訂閱產品類型: 月訂閱、年訂閱
    - 確認定價策略
    - 確認免費試用設定: 7 天免費試用
- **Apple & Google 開發者帳號準備**
    - 確認 Apple Developer Program 狀態
    - 確認 Google Play Console 存取權限
    - 準備 App Store Connect 訂閱設定
- **環境變數與金鑰管理**
    - 規劃 API Keys 儲存方式
    - 設定開發環境 vs 正式環境區分
    - 準備 .env 配置

### 產出文件

- 技術選型決策文件
- 環境設定檢查清單
- 風險緩解計劃
- React Native 版本降級評估報告

### 參考資源

- 成功案例 Podfile: `no99_archive/Podfile`
- 成功案例 AppDelegate: `no99_archive/AppDelegate.swift`
- 問題追蹤報告: `no99_archive/ios_build_fix_report_20251219.md`

### 驗證標準

- 所有開發者帳號已就緒
- 技術方案經過驗證可行
- 團隊對方案達成共識

---

## 階段 1: RevenueCat 基礎整合

### 目標

建立付費權限管理的核心邏輯，獨立於 Firebase 運作。

### RevenueCat Dashboard 設定

- **建立專案**
    - 建立 SuSuGiGi App 專案
    - 連結 Apple App Store
    - 連結 Google Play Store
- **產品設定**
    - 建立月訂閱產品
    - 建立年訂閱產品
    - 設定免費試用期間
- **Entitlement 設定**
    - 建立 Entitlement ID: premium
    - 關聯訂閱產品至 premium entitlement
- **API Keys**
    - 取得 iOS API Key
    - 取得 Android API Key
    - 記錄至安全儲存位置

### 程式碼實作

**更新 revenueCat.ts 服務層:**
- 移除 IS_MOCK_MODE 標記
- 實作 `getOfferings` 方法取得產品列表
- 實作 `purchasePackage` 購買邏輯
- 實作 `restorePurchases` 恢復購買邏輯
- 實作錯誤處理與例外狀況
- 實作離線狀態處理

**更新 PremiumContext.tsx:**
- 加入 `expirationDate` 狀態追蹤
- 實作 `checkPremiumStatus` 純本地計算方法
- 實作離線過期檢查 TTL 邏輯
- 加入 `rawCustomerInfo` 儲存完整回應
- 實作 `lastChecked` 時間戳記錄

**更新 PaywallScreen.tsx:**
- 串接真實 `getOfferings` API
- 動態顯示 App Store 價格
- 實作購買按鈕互動邏輯
- 實作恢復購買按鈕
- 加入 Loading 與錯誤狀態處理

### 測試項目

- 沙盒環境購買流程測試
- 訂閱成功後 Premium 狀態更新
- 恢復購買功能驗證
- 離線時權限檢查正常運作
- 過期訂閱降級邏輯

### 驗證標準

- 可在 iOS TestFlight 完成沙盒購買
- 可在 Android Internal Testing 完成沙盒購買
- Premium 狀態即時反映於 UI
- 離線過期檢查符合規格

---

## 階段 2: Firebase Auth 整合

### 目標

建立使用者身份驗證系統，實作 Google OAuth 登入。

### Firebase 專案設定

- **建立 Firebase 專案**
    - 於 Firebase Console 建立新專案
    - 設定專案名稱與區域
- **啟用 Authentication**
    - 啟用 Google 登入提供者
    - 設定 OAuth 同意畫面
- **iOS 設定**
    - 註冊 iOS App
    - 下載 GoogleService-Info.plist
    - 設定 URL Schemes
- **Android 設定**
    - 註冊 Android App
    - 下載 google-services.json
    - 設定 SHA-1 憑證指紋

### SDK 安裝與設定

> [!NOTE]
> **基於成功案例:** 以下步驟參考已驗證的整合方案

**React Native 版本處理:**
- **IF 同意降級:** 執行 `npm install react-native@0.79.6`
- **IF 保持現版:** 採用 Firebase Web SDK 備用方案

**安裝 Native Firebase SDK:**
```bash
npm install @react-native-firebase/app@^23.4.0
npm install @react-native-firebase/auth@^23.4.0
npm install @react-native-firebase/firestore@^23.4.0
npm install @react-native-google-signin/google-signin
```

**iOS Podfile 配置:**
- 加入 static frameworks 清單
- 設定 pre_install hook 強制 static linkage
- 明確宣告 Firebase pods
- 參考範例: `no99_archive/Podfile`

**關鍵 Podfile 片段:**
```ruby
static_frameworks = [
  'FirebaseAuthInterop',
  'FirebaseAppCheckInterop',
  'FirebaseCore',
  'FirebaseCoreExtension',
  'FirebaseAuth',
  'GoogleUtilities',
  'RecaptchaInterop',
  'FirebaseCoreInternal',
  'FirebaseInstallations',
  'GoogleDataTransport',
  'nanopb'
]

pre_install do |installer|
  installer.pod_targets.each do |pod|
    if static_frameworks.include?(pod.name)
      def pod.build_type
        Pod::BuildType.new(:linkage => :static, :packaging => :framework)
      end
    end
  end
end
```

**iOS AppDelegate.swift 配置:**
- 匯入 `FirebaseCore` 和 `FirebaseAuth`
- 在 `didFinishLaunchingWithOptions` 呼叫 `FirebaseApp.configure()`
- 參考範例: `no99_archive/AppDelegate.swift`

**Android 配置:**
- 將 `google-services.json` 放入 `android/app/`
- 修改 `android/build.gradle` 加入 Google Services plugin
- 修改 `android/app/build.gradle` 套用 plugin

### 程式碼實作

**更新 firebase.ts 服務層:**
- 移除所有 Mock 實作
- 實作真實 Firebase Auth 初始化
- 實作 `signInWithGoogle` 方法
- 實作 `signOut` 方法
- 實作 `onAuthStateChanged` 監聽器

**整合 Google Sign-In:**
- 設定 Google Sign-In 配置
- 實作 OAuth Token 取得流程
- 實作 Firebase Credential 轉換

**更新 AuthContext.tsx:**
- 連接真實 Firebase Auth
- 實作 `onAuthStateChanged` 訂閱
- 同步使用者資料至 WatermelonDB
- 整合 RevenueCat identify 邏輯
- 實作強健的使用者建立流程

**實作 LoginScreen:**
- 建立 Google 登入按鈕 UI
- 實作登入流程互動
- 實作錯誤提示訊息
- 實作 Loading 狀態顯示
- 實作 Redirect Flow 參數處理

### 首次登入流程實作

**本地資料庫同步:**
- 檢查 users collection 是否存在使用者
- **IF 不存在:** 建立新使用者記錄
- **IF 不存在:** 建立預設 settings 記錄
- **IF 不存在:** 執行 seedInitialData
- 更新 lastLoginAt 時間戳

**RevenueCat 識別:**
- 呼叫 `Purchases.configure` 傳入 userId
- 呼叫 `getCustomerInfo` 取得權限狀態
- 更新 PremiumContext

### 測試項目

- Google 登入成功流程
- 使用者資料正確寫入本地 DB
- RevenueCat 正確識別使用者 UID
- 登出後清除狀態
- 錯誤處理: 網路中斷時登入

### 驗證標準

- Google OAuth 流程完整運作
- AuthContext.user 正確更新
- RevenueCat CustomerInfo 與 Firebase UID 綁定
- 本地資料庫與雲端使用者關聯

---

## 階段 3: Firestore 資料同步

### 目標

實作雲端備份與跨裝置同步的基礎設施。

### Firestore 設定

- **啟用 Firestore Database**
    - 選擇資料庫模式: Native Mode
    - 選擇區域: asia-east1 或 asia-northeast1
- **建立 Security Rules**
    - users collection 僅限本人讀寫
    - 實作 premium 權限檢查
    - 防止未授權存取
- **建立索引**
    - users collection 基本索引
    - 依據查詢需求建立複合索引

### Users Collection Schema 實作

**基本資料欄位:**
- `uid`: Firebase Auth UID
- `email`: 使用者 Email
- `displayName`: 顯示名稱
- `photoURL`: 大頭照 URL
- `provider`: 固定為 google.com

**偏好設定欄位:**
- `preferences.language`: 介面語言
- `preferences.currency`: 主要貨幣
- `preferences.timezone`: 時區
- `preferences.theme`: 主題設定

**RevenueCat 權限欄位:**
- `rc_entitlements`: RevenueCat 自動寫入
- `rc_active_subscriptions`: 啟用中訂閱列表

**系統欄位:**
- `createdAt`: 建立時間戳
- `updatedAt`: 更新時間戳

### RevenueCat Firebase Extension

- **安裝 Extension**
    - 於 Firebase Extensions 市場搜尋 RevenueCat
    - 安裝 RevenueCat Integration Extension
    - 設定 API Key
- **配置 Webhook**
    - 設定目標 Collection: users
    - 確認欄位映射正確
    - 測試 Webhook 連線
- **測試同步**
    - 執行沙盒購買
    - 確認 `rc_entitlements` 自動寫入
    - 確認過期後自動移除

### 程式碼實作

**首次登入使用者建立:**
- 實作重試機制: 最多 3 次
- **嘗試 1:** 建立 User Document
- **IF 失敗:** 等待後重試
- **IF 3 次皆失敗:** 自動登出並提示錯誤

**Firestore Listener 實作:**
- 於 AuthContext 加入 `onSnapshot` 監聽
- 監聽路徑: `users/{uid}`
- **當 rc_entitlements 變更:**
    - 解析新的權限狀態
    - 呼叫 PremiumContext.refreshStatus
    - 觸發 UI 重繪

**偏好設定同步:**
- 本地修改後立即寫入 Firestore
- 雲端變更透過 listener 更新本地
- 實作衝突解決: 雲端優先

### SyncEngine 基礎框架

**啟動與停止邏輯:**
- `syncEngine.start()`: 僅在 isPremium 時呼叫
- `syncEngine.stop()`: 降級時呼叫
- 監聽權限變更自動切換

**初步同步功能:**
- 實作連線狀態檢查
- 實作 timestamp 比對邏輯
- 實作基礎上傳框架
- 實作基礎下載框架

### 升級與降級處理

**升級至 Premium:**
- 觸發時機: RevenueCat entitlements.active 包含 premium
- **行為:**
    - 呼叫 `syncEngine.start()`
    - 執行 Initial Sync 上傳全部本地資料
    - 開始監聽雲端變更

**降級至 Free:**
- 觸發時機: RevenueCat entitlements.active 不含 premium
- **行為:**
    - 呼叫 `syncEngine.stop()`
    - 停止所有雲端監聽
    - 保留本地資料不刪除

### 測試項目

- 購買 Premium 後 Firestore 自動建立權限
- PremiumContext 即時更新
- 偏好設定跨裝置同步
- 升級後觸發 Initial Sync
- 降級後 Sync 停止

### 驗證標準

- RevenueCat Webhook 延遲低於 5 分鐘
- 偏好變更同步延遲低於 2 秒
- 升級降級邏輯符合規格
- Security Rules 通過測試

---

## 階段 4: 完整同步引擎

### 目標

實作帳務資料的完整雲端備份與跨裝置同步。

### Firestore Collections Schema 設計

**transactions collection:**
- 路徑: `users/{uid}/transactions/{transactionId}`
- 欄位: 所有交易欄位 + updatedOn 時間戳
- 索引: updatedOn, transactionDate

**accounts collection:**
- 路徑: `users/{uid}/accounts/{accountId}`
- 欄位: 所有帳戶欄位 + updatedOn
- 索引: updatedOn, sortOrder

**categories collection:**
- 路徑: `users/{uid}/categories/{categoryId}`
- 欄位: 所有類別欄位 + updatedOn
- 索引: updatedOn, sortOrder

**recurring_settings collection:**
- 路徑: `users/{uid}/recurring_settings/{settingId}`
- 欄位: schedule 相關欄位 + updatedOn
- 索引: updatedOn, nextOccurrence

### 增量同步邏輯

**上傳邏輯:**
- 查詢本地: `WHERE updatedOn > lastSyncedAt`
- 批次寫入 Firestore: 最多 500 筆
- 更新 lastSyncedAt 時間戳

**下載邏輯:**
- 查詢 Firestore: `WHERE updatedOn > lastSyncedAt`
- 批次寫入本地 DB
- 更新 lastSyncedAt 時間戳

**衝突解決策略:**
- 採用 LWW: Last Write Wins
- 比較 updatedOn 時間戳
- 較新的資料覆蓋較舊資料

### Initial Sync 實作

**觸發時機:**
- Premium 升級時
- 全新裝置登入時

**執行邏輯:**
- **IF 本地有資料 & 雲端無資料:** 完整上傳
- **IF 本地無資料 & 雲端有資料:** 完整下載
- **IF 雙方皆有資料:** 依 updatedOn 合併

**批次處理:**
- 分批處理避免超時
- 每批 500 筆
- 顯示同步進度於 UI

### 錯誤處理與重試

**網路錯誤:**
- 自動重試: 最多 3 次
- 指數退避: 1s, 2s, 4s
- 失敗後顯示錯誤提示

**Quota 超限:**
- 偵測 Firestore quota 錯誤
- 暫停同步並提示使用者
- 隔日自動恢復

**資料衝突:**
- 記錄衝突事件
- 自動採用 LWW 解決
- 不阻擋使用者操作

### 同步狀態管理

**新增 SyncContext:**
- `isSyncing`: 同步進行中
- `lastSyncTime`: 上次同步時間
- `syncProgress`: 同步進度百分比
- `syncError`: 錯誤訊息

**UI 顯示:**
- SettingsScreen 顯示同步狀態
- 提供手動同步按鈕
- 顯示上次同步時間

### 測試項目

- 全新裝置登入拉取雲端資料
- 多裝置同時編輯正確合併
- 大量資料同步效能測試
- 網路中斷時重試機制
- Quota 超限處理

### 驗證標準

- 1000 筆交易同步時間低於 30 秒
- 衝突解決邏輯正確無誤
- 錯誤處理涵蓋所有已知情境
- 使用者體驗流暢無卡頓

---

## 階段 5: 整合測試與優化

### 目標

端到端驗證所有整合功能，確保生產環境可用。

### 端到端測試情境

**情境 1: 新使用者完整流程**
- 下載 App
- Google 登入
- 建立第一筆交易
- 購買 Premium
- 確認資料已備份至雲端
- 於第二台裝置登入
- 確認資料自動下載

**情境 2: 免費使用者升級**
- 免費版使用 3 個月累積資料
- 升級 Premium
- 確認歷史資料完整上傳
- 確認同步引擎啟動

**情境 3: Premium 過期處理**
- 使用 Premium 功能
- 取消訂閱等待過期
- 確認過期後降級為 Free
- 確認本地資料保留
- 確認同步停止

**情境 4: 恢復購買**
- 刪除 App
- 重新安裝
- 登入
- 點擊恢復購買
- 確認 Premium 狀態恢復
- 確認資料自動下載

**情境 5: 長期離線使用**
- 開啟飛航模式
- 使用 App 7 天
- Premium 到期
- 確認離線過期檢查降級
- 確認本地功能仍可用

### 效能優化

**Firestore 讀寫優化:**
- 監控讀寫次數
- 實作智慧同步頻率: 避免 5 分鐘內重複同步
- 合併多次偏好變更為單次寫入

**本地資料庫優化:**
- 檢查 WatermelonDB 查詢效能
- 確認索引設定正確
- 優化 syncEngine 查詢邏輯

**App 啟動優化:**
- 確保 Splash Screen 時間合理
- 非同步載入 Firebase SDK
- 延遲載入非必要模組

### 成本監控

**RevenueCat 成本:**
- 監控 API 呼叫次數
- 確認在免費額度內
- 規劃付費方案升級時機

**Firestore 成本:**
- 每日讀取次數統計
- 每日寫入次數統計
- 儲存空間使用量
- 預估月費用

### 錯誤監控與記錄

**整合 Crashlytics:**
- 安裝 Firebase Crashlytics
- 記錄同步失敗事件
- 記錄購買失敗事件
- 追蹤使用者流程

**關鍵指標追蹤:**
- Premium 轉換率
- 同步成功率
- 平均同步時間
- 錯誤發生率

### 文件更新

**開發文件:**
- 更新 README 設定步驟
- 建立環境變數設定指南
- 建立 Firebase 專案建置指南
- 建立故障排除文件

**程式碼文件:**
- 補充關鍵函式註解
- 建立 API 文件
- 建立架構圖表

**Security Rules 審查:**
- 審查 Firestore Security Rules
- 確認無安全漏洞
- 執行 Rules 單元測試

### 驗證標準

- 所有測試情境通過無錯誤
- Firestore 月成本低於預算
- App 效能符合標準
- 錯誤率低於 1%
- 文件完整可供新成員參考

---

## 風險管理

### 技術風險

**React Native 版本降級風險:**
- **風險:** 現有程式碼可能不相容 0.79.6
- **緩解:** 降級前完整測試所有功能
- **應變:** 如有不相容，維持 0.83.1 改用 Web SDK

**Firebase SDK 相容性:**
- **風險:** iOS Native SDK 整合失敗
- **緩解:** 採用已驗證的 Podfile 配置與 RN 0.79.6
- **應變:** 若仍失敗，改用 Firebase Web SDK

**RevenueCat Webhook 延遲:**
- **風險:** 權限同步延遲超過預期
- **緩解:** 實作本地離線權限檢查
- **應變:** 顯示同步中狀態提示使用者

**Firestore Quota 限制:**
- **風險:** 超過免費額度
- **緩解:** 智慧同步頻率控制
- **應變:** 升級至 Blaze 付費方案

### 商業風險

**Apple 審核拒絕:**
- **風險:** 訂閱流程不符合 App Store 規範
- **緩解:** 詳閱 App Store Review Guidelines
- **應變:** 調整 UI 文案與流程

**使用者隱私問題:**
- **風險:** 資料處理不符合 GDPR
- **緩解:** 實作完整隱私權政策
- **應變:** 加入資料匯出與刪除功能

### 時程風險

**開發延遲:**
- **風險:** 實作時間超過預期
- **緩解:** 分階段驗收，及早發現問題
- **應變:** 調整階段優先順序

---

## 時程規劃建議

### 快速路徑: 4 週

- **第 1 週:** 階段 0 + 階段 1
- **第 2 週:** 階段 2
- **第 3 週:** 階段 3
- **第 4 週:** 階段 4 + 階段 5

### 穩健路徑: 8 週

- **第 1-2 週:** 階段 0 + 階段 1
- **第 3-4 週:** 階段 2
- **第 5-6 週:** 階段 3
- **第 7 週:** 階段 4
- **第 8 週:** 階段 5

### 建議採用

**穩健路徑:** 確保每個階段充分測試與優化。

---

## 成功指標

### 技術指標

- 同步成功率 > 99%
- App 啟動時間 < 3 秒
- Premium 購買流程完成率 > 80%
- Firestore 月成本 < USD 50

### 使用者體驗指標

- 登入流程完成率 > 90%
- 付費牆轉換率 > 5%
- 同步功能滿意度 > 4.5/5
- Crash-free 使用者比例 > 99%

---

## 後續維護計劃

### 定期維護

- 每月檢查 Firestore 使用量
- 每季審查 Security Rules
- 每季更新 SDK 版本
- 每半年審查成本結構

### 功能迭代

- 收集使用者回饋
- 優化同步演算法
- 加入進階訂閱方案
- 實作家庭共享功能

---

**文件結束**
