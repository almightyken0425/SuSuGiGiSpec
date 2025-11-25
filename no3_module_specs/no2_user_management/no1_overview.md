# User Management Module

## 模組目的

- **User Management 模組負責:**
  - **使用者資料儲存:** 在 Firestore 中維護使用者個人資料, Users Collection。
  - **身分驗證邏輯:** 定義首次登入與帳號建立流程。
  - **偏好設定管理:** 定義語言、貨幣、時區等偏好設定的資料結構與更新 API。
  - **RevenueCat 整合:** 為訂閱權限資料預留欄位結構。


### User Management, 即時與文件導向
> **範圍**: 身分、偏好設定、訂閱權限, `users/{uid}`

- **登入與初始化, Login & Init**
  - **時機:** App 啟動或登入時。
  - **行為:** 讀取 `users/{uid}`。若為新用戶，則建立預設文件, Onboarding。
- **偏好設定更新, Update Preferences**
  - **時機:** 使用者修改語言、幣別、主題時。
  - **行為:** 即時寫入 `users/{uid}`。
- **訂閱狀態監聽, Subscription Listener**
  - **時機:** App 運作期間持續監聽。
  - **行為:** 監聽 `users/{uid}` 的 `rc_entitlements` 欄位變更, 由 RevenueCat Server 同步寫入。

### Accounting Data, 批次同步與集合導向
> **範圍**: 交易、帳戶、類別等記帳資料
> **詳見**: `no3_accounting_app/no3_background_logics/no3_batch_sync_spec.md`

- **每日自動同步, Daily Auto Sync**
  - **時機:** App 啟動, Bootstrap 時，若距離上次檢查超過 24 小時。
  - **條件:** 僅限付費會員, Premium。
  - **行為:** 觸發背景批次同步, Delta Sync。
- **手動同步, Manual Sync**
  - **時機:** 使用者在設定頁面點擊「立即同步」。
  - **行為:** 立即觸發批次同步。
- **跨裝置與重裝同步, First Sync**
  - **時機:** 付費會員在全新裝置登入後。
  - **行為:** 下載雲端所有資料至本機。

---

## 互動流程圖

> [!NOTE]
> 詳細互動流程圖請參閱:
> - **User Management:** `no1_interaction_flows/no1_user_management_flows.md`
> - **Accounting App:** `no1_interaction_flows/no2_accounting_flows.md`