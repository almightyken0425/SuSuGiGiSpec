# User Management Module

## 模組目的

- **User Management 模組負責:**
  - **使用者資料儲存:** 在 Firestore 中維護使用者個人資料, Users Collection。
  - **身分驗證邏輯:** 定義首次登入與帳號建立流程。
  - **偏好設定管理:** 定義語言、貨幣、時區等偏好設定的資料結構與更新 API。
  - **RevenueCat 整合:** 為訂閱權限資料預留欄位結構。

> [!NOTE]
> 本模組專注於 **後端規格, Backend Specs**，包含 Schema、邏輯流程與 API 定義。
> 前端 UI 實作, 如登入畫面、設定畫面 的規格文件保留於 **Accounting App** 模組中。

---

## 實作重點

- **Firestore Users Collection:**
  - **單一真理來源:** 所有使用者偏好如 Language, Currency, TimeZone 皆以此 Collection 為準。
  - **RevenueCat 同步:** 自動寫入訂閱狀態，不需手動維護。

- **首次登入邏輯:**
  - **冪等性:** 確保重複觸發也不會破壞現有資料。
  - **預設值:** 新用戶自動帶入預設偏好如 zh-TW, TWD, Asia/Taipei。

- **偏好設定更新:**
  - **API:** 提供簡單的介面供前端更新偏好。

---

## 系統與 Firestore 互動時機

App 與 Firestore 的互動分為兩大類：**User Management, 即時互動** 與 **Accounting Data, 批次同步**。

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
> **詳見**: `no2_accounting_app/no3_background_logics/no3_batch_sync_spec.md`

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

```mermaid
graph TB
    subgraph client["App Client"]
        Bootstrap[App Launch / Bootstrap]
        UserAction[User Settings Action]
        SyncEngine[Sync Engine (Background)]
    end

    subgraph firestore["Firestore DB"]
        UserDoc[User Doc (users/{uid})]
        DataColl[Data Collections (transactions, etc.)]
    end

    %% User Management Interactions
    Bootstrap -->|"1. Check/Create (Real-time)"| UserDoc
    UserAction -->|"2. Update Prefs (Real-time)"| UserDoc
    UserDoc -.->|"3. Listen Subscription"| Bootstrap

    %% Accounting Data Interactions
    Bootstrap -.->|"4. Trigger Auto Sync (Daily)"| SyncEngine
    UserAction -.->|"5. Trigger Manual Sync"| SyncEngine
    
    SyncEngine ==>|"6. Batch Upload (Delta)"| DataColl
    DataColl ==>|"7. Batch Download (Delta)"| SyncEngine
```