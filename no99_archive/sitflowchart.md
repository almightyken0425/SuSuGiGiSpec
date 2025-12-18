# 提款審核流程規格：手動與自動模式對照

---

## 畫面目標

- 規範提款單在不同審核模式下的狀態流轉邏輯。
- 當開啟「自動財務審核」時，簡化審核步驟，並明確 API 失敗或三方拒絕後的處理路徑。
- 支援 Metronic 等不具備帳戶所有權的第三方金流服務整合。

---

## 邏輯定義

- **提款單狀態說明:**
    - `Pending`: 玩家發起提款後的初始狀態。
    - `Lock`: 提款單進入審核鎖定狀態。
    - `Checked`: Risk 團隊審核同意後的狀態。
    - `Approve`: Finance 團隊審核同意，並已向三方發起提款申請或執行手動出款後的最終核准狀態。
    - `Decline`: 任何階段拒絕或三方系統異常後的最終拒絕狀態。

---

## 手動財務審核流程 (Auto OFF)

- **行為描述:** 需 Risk 與 Finance 兩關人工審核。若三方拒絕，流程退回至 `Checked` 供再次處理。
- **流程圖:**

```mermaid
graph TD
    %% 節點定義
    Start(["Player Submit Withdrawal"])
    Pending("Status: Pending")
    
    RiskLockActionBox["Risk Lock"]
    RiskLock("Status: Locked")
    
    RiskAction{"Risk Approve/Reject"}
    Checked("Status: Checked")
    
    FinanceLockActionBox["Finance Lock"]
    FinanceLock("Status: Locked")
    
    FinanceAction{"Finance Approve/Reject"}
    ApproveReq("Status: Approve<br/>(Requesting 3rd Party)")
    Decline("Status: Decline")
    Success("Status: Approve<br/>(Success)")
    Callback{"Callback / API Result"}

    Start --> Pending
    
    Pending --> RiskLockActionBox
    RiskLockActionBox --> RiskLock
    
    RiskLock --> RiskAction
    
    RiskAction -->|"Approve"| Checked
    
    Checked --> FinanceLockActionBox
    FinanceLockActionBox --> FinanceLock
    
    FinanceLock --> FinanceAction
    
    FinanceAction -->|"Approve<br/>(With Selected Channel)"| ApproveReq

    RiskAction -->|"Reject"| Decline
    FinanceAction -->|"Reject"| Decline
    
    ApproveReq -->|"Wait Response"| Callback

    Callback -->|"Approve"| Success
    Callback -->|"Reject"| Checked

    style Decline fill:#f96,stroke:#333
    style Success fill:#9f9,stroke:#333
    style RiskLockActionBox fill:#fff,stroke:#333,stroke-dasharray: 5 5
    style FinanceLockActionBox fill:#fff,stroke:#333,stroke-dasharray: 5 5
```

---

## 自動財務審核流程 (Auto ON)

- **行為描述:** Risk 同意後系統背景自動處理。若三方失敗，則**直接拒絕**不退回人工。
- **流程圖:**

```mermaid
graph TD
    %% 節點定義
    StartAuto(["Player Submit Withdrawal"])
    PendingAuto("Status: Pending")
    
    RiskLockActionBoxAuto["Risk Lock"]
    RiskLockAuto("Status: Locked")
    
    RiskActionAuto{"Risk Approve/Reject"}
    ApproveAuto("Status: Checked")
    ApproveReqAuto("Status: Approve<br/>(Requesting 3rd Party)")
    DeclineAuto("Status: Decline")
    SuccessAuto("Status: Approve<br/>(Success)")
    CallbackAuto{"Callback / API Result"}

    StartAuto --> PendingAuto
    
    PendingAuto --> RiskLockActionBoxAuto
    RiskLockActionBoxAuto --> RiskLockAuto
    
    RiskLockAuto --> RiskActionAuto
    
    %% 高亮自動化路徑
    RiskActionAuto ==>|"Approve (Auto Trigger)"| ApproveAuto
    ApproveAuto ===>|"Auto Request"| ApproveReqAuto

    RiskActionAuto -->|"Reject"| DeclineAuto
    
    ApproveReqAuto -->|"Wait Response"| CallbackAuto

    CallbackAuto -->|"Approve"| SuccessAuto
    
    %% 高亮報廢路徑
    CallbackAuto --x|"Reject / API Fail"| DeclineAuto

    %% 樣式與連結美化
    %% linkStyle 索引 (基於連接線出現順序):
    %% 0: StartAuto -> PendingAuto
    %% 1: PendingAuto -> RiskLockActionBoxAuto
    %% 2: RiskLockActionBoxAuto -> RiskLockAuto
    %% 3: RiskLockAuto -> RiskActionAuto
    %% 4: RiskActionAuto ==> ApproveAuto
    %% 5: ApproveAuto ===> ApproveReqAuto
    %% 6: RiskActionAuto --> DeclineAuto
    %% 7: ApproveReqAuto --> CallbackAuto
    %% 8: CallbackAuto --> SuccessAuto
    %% 9: CallbackAuto --x DeclineAuto

    linkStyle 4 stroke:#2196f3,stroke-width:4px;
    linkStyle 5 stroke:#2196f3,stroke-width:4px;
    linkStyle 9 stroke:#f44336,stroke-width:2px;

    style DeclineAuto fill:#f96,stroke:#333
    style SuccessAuto fill:#9f9,stroke:#333
    style ApproveAuto fill:#e3f2fd,stroke:#2196f3
    style RiskLockActionBoxAuto fill:#fff,stroke:#333,stroke-dasharray: 5 5
```

---

## 核心行為細節對照

- **手動審核 (OFF):**
    - Finance 點擊同意時，必須跳出彈窗選擇 `Payment Channel`。
    - **IF** 三方 Reject: 流程連回 `Checked`，由財務重新鎖定並選擇其他通道。
- **自動審核 (ON):**
    - Risk 同意後，系統背景自動執行 Finance 鎖定與同意，完全跳過人工 Finance UI。
    - **IF** 三方 Reject/API Fail: 狀態**直接轉為 `Decline`**，視為該筆訂單終止，不再退回人工處理。

---

**文件結束**
