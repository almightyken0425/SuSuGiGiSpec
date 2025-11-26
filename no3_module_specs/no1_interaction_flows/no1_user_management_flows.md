# User Management Interaction Flows

## 首次登入流程, First Login Flow

> **來源**: 移自 `no2_user_management/no2_first_login_flow.md`

```mermaid
sequenceDiagram
    participant U as 使用者
    participant App as App
    participant Auth as Firebase Auth
    participant DB as Firestore

    U->>App: 點擊「Google 登入」
    App->>Auth: signInWithGoogle()
    Auth->>App: 返回 User
    App->>DB: 查詢 users/{uid}
    
    alt 使用者文件不存在
        DB->>App: 文件不存在
        App->>DB: 建立使用者文件
        DB->>App: 建立成功
        App->>U: 導航至主畫面
    else 使用者文件已存在
        DB->>App: 返回現有資料
        App->>U: 導航至主畫面
    end
```

---

## 偏好設定更新流程, Update Preferences Flow

> **情境**: 使用者修改語言、貨幣、主題時。

```mermaid
sequenceDiagram
    participant U as 使用者
    participant App as App
    participant DB as Firestore

    U->>App: 修改偏好設定 (語言/貨幣/主題)
    App->>App: 更新本地 State/Cache
    App->>DB: 寫入 users/{uid}/preferences
    
    alt 寫入成功
        DB-->>App: ACK
    else 寫入失敗 (離線)
        App->>App: 標記 Dirty, 待 Sync
    end
```

---

## 訂閱狀態監聽流程, Subscription Listener Flow

> **情境**: App 運作期間持續監聽權限變更。

```mermaid
sequenceDiagram
    participant RC as RevenueCat Server
    participant DB as Firestore
    participant App as App

    RC->>DB: Webhook 更新 rc_entitlements
    DB->>App: onSnapshot (users/{uid})
    App->>App: 更新 PremiumContext
    
    alt 權限升級 (Tier 0 -> 1)
        App->>App: 解鎖 Premium 功能
        App->>App: 觸發 Initial Batch Sync (上傳本地 -> 下載雲端)
    else 權限降級 (Tier 1 -> 0)
        App->>App: 鎖定 Premium 功能
        App->>App: 停止 Sync Engine (Stop & Freeze)
    end
```

---

## App 生命週期與資料同步行為, App Lifecycle & Sync Behavior

> **目的**: 確保在 App 各種啟動狀態下，使用者權限與資料狀態能維持最終一致性。

### 1. 冷啟動, Cold Start

> **情境**: App 被完全關閉後重新開啟。

```mermaid
sequenceDiagram
    participant U as 使用者
    participant App as App
    participant SDK as Firestore SDK
    participant Cloud as Firestore Cloud

    U->>App: 開啟 App
    App->>SDK: 初始化 & 註冊 onSnapshot
    
    rect rgb(240, 248, 255)
        note right of SDK: 連線建立階段
        SDK->>Cloud: 建立連線 (Handshake)
        Cloud-->>SDK: 連線成功
    end

    rect rgb(255, 250, 240)
        note right of SDK: 資料同步階段
        Cloud->>SDK: 推送最新 Snapshot (含 rc_entitlements)
        SDK->>App: 觸發 onSnapshot Callback
        App->>App: 更新 PremiumContext
        App->>App: 執行 升級/降級 邏輯
    end
```

### 2. 熱啟動, Warm Start (Background to Foreground)

> **情境**: App 在背景執行 (Suspended) 後回到前景。

```mermaid
sequenceDiagram
    participant U as 使用者
    participant App as App
    participant SDK as Firestore SDK
    participant Cloud as Firestore Cloud

    note over App, Cloud: App 在背景 (連線可能中斷)
    
    U->>App: 切換回 App (Foreground)
    App->>SDK: App 狀態變為 Active
    
    alt 連線已斷開
        SDK->>Cloud: 自動重連
        Cloud-->>SDK: 連線恢復
        Cloud->>SDK: 推送背景期間的變更
    else 連線仍存活
        SDK->>Cloud: 心跳檢查 / Sync 請求
        Cloud->>SDK: 推送最新狀態
    end

    SDK->>App: 觸發 onSnapshot Callback
    App->>App: 更新 PremiumContext (修正背景期間的狀態差異)
```

### 3. 離線啟動, Offline Launch

> **情境**: 無網路環境下開啟 App。

- **行為**:
    1.  **讀取快照**: SDK 無法連線，直接回傳 **本地快照 (Local Cache)** 給 App。
    2.  **暫時狀態**: App 使用舊的權限狀態運作 (若上次是 Premium，則暫時維持 Premium)。
    3.  **恢復連線**: 當網路恢復時，SDK 自動背景連線並同步。
    4.  **最終一致**: 收到最新 Snapshot 後，App 立即更新 Context 並執行對應的鎖定或解鎖邏輯。
