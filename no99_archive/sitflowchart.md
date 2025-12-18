# 提款審核流程規格：手動與自動財務審核對照

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
- **模式差異:**
    - **非自動審核模式:** 需要 Risk 與 Finance 分別執行 鎖定與同意。
    - **自動審核模式:** Risk 同意後，系統自動以预設 `Payment Channel` 執行 Finance 同意邏輯。

---

## 流程對照圖

```mermaid
graph TD
    %% 定義節點
    Start([玩家發起提款]) --> Pending(Pending)
    
    subgraph Mode_Manual [手動財務審核模式]
        Pending --> Risk_Lock[Risk 鎖定]
        Risk_Lock --> Risk_Action{Risk 審核}
        Risk_Action -- 拒絕 --> Decline1([Decline])
        Risk_Action -- 同意 --> Checked(Checked)
        
        Checked --> Finance_Lock[Finance 鎖定]
        Finance_Lock --> Finance_Action{Finance 審核}
        Finance_Action -- 拒絕 --> Decline2([Decline])
        Finance_Action -- 同意 - 選擇 Channel --> ApproveMan(Approve <br/>並對三方發起申請)
        
        ApproveMan --> Callback{三方 Callback}
        Callback -- Approve --> Success([更新 Vendor TX ID])
        Callback -- Reject --> Checked
    end

    subgraph Mode_Auto [自動財務審核模式]
        Pending_Auto(Pending) --> Risk_Lock_Auto[Risk 鎖定]
        Risk_Lock_Auto --> Risk_Action_Auto{Risk 審核}
        Risk_Action_Auto -- 拒絕 --> Decline_Auto([Decline])
        Risk_Action_Auto -- 同意 - 自動選擇 Channel --> ApproveAuto(Approve <br/>並對三方發起申請)
        
        ApproveAuto --> Callback_Auto{三方 Callback}
        Callback_Auto -- Approve --> Success_Auto([更新 Vendor TX ID])
        Callback_Auto -- Reject/API Fail --> Decline_Auto
    end

    %% 樣式美化
    style Decline1 fill:#f96,stroke:#333
    style Decline2 fill:#f96,stroke:#333
    style Decline_Auto fill:#f96,stroke:#333
    style Success fill:#9f9,stroke:#333
    style Success_Auto fill:#9f9,stroke:#333
```

---

## 核心行為細節

- **手動審核模式行為:**
    - Finance 點擊同意時，必須跳出彈窗選擇 `Payment Channel`。
    - 若三方 Callback 回傳 `Reject`，則狀態退回至 `Checked` 供財務重新處理。
- **自動審核模式行為:**
    - 系統應提供「預設自動提款通道」設定。
    - Risk 同意後，不需 Finance 干預，系統自動鎖定並同意。
    - **IF** 三方 API 建立提款單失敗 **OR** 回傳 `Reject`:
        - 狀態直接轉為 `Decline`。
        - **行為:** 為了與 T1 包網平台的簡便流程對齊，此模式不再退回處理，視為出款失敗。

---

**文件結束**
