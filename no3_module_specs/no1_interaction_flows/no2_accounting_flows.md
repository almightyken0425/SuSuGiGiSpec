# Accounting App Interaction Flows

## App 啟動流程, App Bootstrap Flow

> **來源**: 參考 `no3_accounting_app/no3_background_logics/no1_app_bootstrap_flow.md`

```mermaid
graph TD
    Start[使用者開啟 App] --> Splash[顯示 Splash]
    Splash --> CheckAuth{檢查 Auth State}
    
    CheckAuth -- 未登入 --> Login[導航: LoginScreen]
    CheckAuth -- 已登入 --> Home[導航: HomeScreen]
    
    Home --> LoadDB[讀取本機 DB 顯示 UI]
    LoadDB --> CheckPremium{檢查 Premium}
    
    CheckPremium -- No --> End[結束]
    CheckPremium -- Yes --> Recurring{檢查定期交易}
    
    Recurring -- 需補產生 --> GenRecurring[執行補產生邏輯]
    GenRecurring --> AutoSync{檢查自動同步}
    Recurring -- 無需 --> AutoSync
    
    AutoSync -- > 24hr --> TriggerSync[觸發批次同步]
    AutoSync -- < 24hr --> End
```

---

## 批次同步流程, Batch Sync Flow

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
