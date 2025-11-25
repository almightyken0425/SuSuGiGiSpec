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
    App->>App: 解鎖/鎖定 功能
```
