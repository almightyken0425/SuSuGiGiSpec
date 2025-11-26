# App Interaction Flows

## 1. 使用者管理流程, User Management Flows

### 首次登入流程, First Login Flow

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
    
    alt 使用者文件已存在
        DB->>App: 返回現有資料
        App->>U: 導航至主畫面
    else 使用者文件不存在 (Empty)
        loop Max 3 Times
            App->>DB: 嘗試建立使用者文件
            alt 建立成功
                App->>DB: 再次查詢 (Re-fetch)
                DB->>App: 返回新建立資料
                App->>U: 導航至主畫面
                Note right of App: 成功跳出迴圈
            else 建立失敗
                App->>App: 等待後重試 (Exponential Backoff)
            end
        end
        
        opt 3次皆失敗
            App->>U: 顯示錯誤提示 (請稍後再試)
            App->>Auth: 登出 (清除無效狀態)
        end
    end
```

### 偏好設定更新流程, Update Preferences Flow

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

### 訂閱狀態監聽流程, Subscription Listener Flow

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

## 2. 記帳與同步流程, Accounting & Sync Flows
    GenRecurring --> AutoSync{檢查自動同步}
    Recurring -- 無需 --> AutoSync
    
    AutoSync -- > 24hr --> TriggerSync[觸發批次同步]
    AutoSync -- < 24hr --> End
```

### 批次同步流程, Batch Sync Flow

> **來源**: 參考 `no3_accounting_app/no3_background_logics/no3_batch_sync_spec.md`

```mermaid
sequenceDiagram
    participant App as App
    participant LocalDB as Local DB
    participant Cloud as Firestore

    Note over App: 觸發同步 (手動/自動)
    
    rect rgb(200, 220, 240)
        Note right of App: 上傳階段 (Upload)
        App->>LocalDB: 查詢 updatedOn > lastSyncTimestamp
        LocalDB-->>App: 回傳變更資料
        App->>Cloud: 批次寫入 (Batch Write)
    end
    
    rect rgb(220, 240, 200)
        Note right of App: 下載階段 (Download)
        App->>Cloud: 查詢 updatedOn > lastSyncTimestamp
        Cloud-->>App: 回傳雲端變更
        App->>LocalDB: 批次 Upsert (LWW 策略)
    end
    
    rect rgb(240, 220, 220)
        Note right of App: 完成階段 (Finalize)
        App->>LocalDB: 更新 lastSyncTimestamp
        App->>App: 更新 UI 狀態
    end
```

---

## 3. 系統行為, System Behaviors

### App 生命週期與資料同步行為, App Lifecycle & Sync Behavior

> **目的**: 確保在 App 各種啟動狀態下，使用者權限與資料狀態能維持最終一致性。

#### 冷啟動, Cold Start

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

#### 熱啟動, Warm Start (Background to Foreground)

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

#### 離線啟動, Offline Launch

> **情境**: 無網路環境下開啟 App。

- **行為**:
    1.  **讀取快照**: SDK 無法連線，直接回傳 **本地快照 (Local Cache)** 給 App。
    2.  **暫時狀態**: App 使用舊的權限狀態運作 (若上次是 Premium，則暫時維持 Premium)。
    3.  **恢復連線**: 當網路恢復時，SDK 自動背景連線並同步。
    4.  **最終一致**: 收到最新 Snapshot 後，App 立即更新 Context 並執行對應的鎖定或解鎖邏輯。

---

## 4. 全域互動總覽, Unified Interaction Overview

> **說明**: 將上述所有流程整合為單一視圖，展示各角色在不同情境下的互動關係。

```mermaid
sequenceDiagram
    autonumber
    participant U as User
    participant App as App (Client)
    participant Local as Local DB
    participant Auth as Firebase Auth
    participant Cloud as Firestore
    participant RC as RevenueCat

    box "Client Side" #f9f9f9
        participant U
        participant App
        participant Local
    end
    
    box "Server Side" #ececec
        participant Auth
        participant Cloud
        participant RC
    end

    %% --- 1. App Bootstrap & Lifecycle (Local-First) ---
    note over U, Cloud: 1. App 啟動與生命週期 (Bootstrap & Lifecycle)
    U->>App: 開啟 App (Cold/Warm Start)
    App->>App: 顯示 Splash (Logo)
    App->>Local: 讀取資料 & 顯示 UI (Home)
    
    App->>Auth: 背景檢查 Auth State
    
    alt 已登入 (Logged In)
        App->>Cloud: 註冊 onSnapshot (User/Entitlements)
        Cloud-->>App: 推送最新 Snapshot
        App->>App: 更新 PremiumContext
        
        opt isPremium == True
            App->>App: 檢查定期交易 & 自動同步
        end
    else 未登入 (Guest)
        App->>App: 維持訪客模式 (僅本地功能)
    end

    %% --- 2. Login Interaction (Modal) ---
    note over U, Cloud: 2. 登入互動 (Login Modal)
    
    U->>App: 觸發登入 (Settings/Paywall/Sync)
    App->>App: 顯示 Login Modal
    U->>App: 點擊 Google 登入
    App->>Auth: signInWithGoogle()
    Auth-->>App: 返回 User Token
    
    App->>Cloud: 查詢 User Profile
    alt Profile 已存在
        Cloud-->>App: 返回現有資料
    else Profile 不存在 (Empty)
        loop Max 3 Times
            App->>Cloud: 嘗試建立 User Profile
            alt 建立成功
                App->>Cloud: 再次查詢 (Re-fetch)
                Cloud-->>App: 返回新建立資料
                Note right of App: 成功跳出迴圈
            else 建立失敗
                App->>App: 等待後重試
            end
        end
        
        opt 3次皆失敗
            App->>U: 顯示錯誤 & 自動登出
        end
    end
    
    App->>App: 關閉 Login Modal
    App->>App: 綁定 Local Data to User (若需)
    App->>App: 觸發 Initial Sync (若為 Premium)

    %% --- 3. User Interactions ---
    note over U, Cloud: 3. 使用者互動 (User Actions)
    
    par 修改偏好設定 (Update Preferences)
        U->>App: 修改語言/貨幣
        App->>Local: 更新 Local State
        App->>Cloud: 寫入 users/{uid}/preferences
    and 手動同步 (Manual Sync)
        U->>App: 點擊「立即同步」
        App->>Local: 查詢變更 (Upload)
        Local-->>App: 回傳 Delta
        App->>Cloud: 批次寫入
        App->>Cloud: 查詢變更 (Download)
        Cloud-->>App: 回傳 Delta
        App->>Local: 寫入 Local DB
    end

    %% --- 4. External Events ---
    note over U, RC: 4. 外部事件 (External Events)
    RC->>Cloud: Webhook: 訂閱狀態變更
    Cloud->>App: onSnapshot 通知 (Real-time)
    App->>App: 更新 PremiumContext
    alt 升級 (Upgrade)
        App->>App: 解鎖功能 & 觸發 Initial Sync
    else 降級 (Downgrade)
        App->>App: 鎖定功能 & 停止 Sync
    end
```

