# 提款審核流程規格：全域流程圖 (手動/自動對照)

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

## 全域流程圖

```mermaid
graph TD
    subgraph Platform_System [平台系統行為]
        %% 初始步驟
        Start([玩家發起提款]) --> Pending(Pending)
        Pending --> Risk_Lock[Risk 鎖定]
        Risk_Action{Risk 審核}
        Risk_Lock --> Risk_Action
        
        %% Risk 同意後檢查
        Check_Auto{是否開啟<br/>Auto Approve?}
        Risk_Action -- 同意 --> Check_Auto
        
        %% 分支 1: 手動財務審核 (Auto OFF)
        Checked(Checked <br/>Finance 尚未鎖定)
        Check_Auto -- "OFF (手動)" --> Checked
        Finance_Lock[Finance 鎖定]
        Checked --> Finance_Lock
        Finance_Action{Finance 審核}
        Finance_Lock --> Finance_Action
        
        %% 分支 2: 自動財務審核 (Auto ON)
        Approve_Auto_Flow(Approve <br/>系統自動選擇 Channel)
        Check_Auto -- "ON (自動)" --> Approve_Auto_Flow
        
        %% 共同發送 API 點
        Approve_Request(Approve <br/>對三方發起申請)
        Finance_Action -- 同意 - 選擇 Channel --> Approve_Request
        Approve_Auto_Flow --> Approve_Request

        %% 拒絕與成功最終站
        Decline_Final([Decline])
        Risk_Action -- 拒絕 --> Decline_Final
        Finance_Action -- 拒絕 --> Decline_Final
        
        Success([更新 Vendor TX ID])

        %% 異常處理分支 (模式判定)
        Fail_Branch{模式判定}
        Fail_Branch -- "手動模式 (Auto OFF)" --> Checked
        Fail_Branch -- "自動模式 (Auto ON)" --> Decline_Final
    end

    subgraph Third_Party [三方金流行為 - Metronic]
        Approve_Request --> Callback{三方 Callback <br/>/ API 結果}
    end

    %% 回傳平台處理
    Callback -- Approve --> Success
    Callback -- Reject / API Fail --> Fail_Branch

    %% 樣式美化
    style Decline_Final fill:#f96,stroke:#333
    style Success fill:#9f9,stroke:#333
    style Check_Auto fill:#fff9c4,stroke:#333
    style Fail_Branch fill:#fff9c4,stroke:#333
    style Platform_System fill:#f5f5f5,stroke:#999,stroke-dasharray: 5 5
    style Third_Party fill:#e1f5fe,stroke:#01579b
```

---

## 核心行為細節

- **手動審核流程細節:**
    - Finance 點擊同意時，必須跳出彈窗選擇 `Payment Channel`。
    - 若三方 Callback 回傳 `Reject`，則狀態退回至 `Checked` 供財務人員手動再次鎖定/重選通道。
- **自動審核流程細節:**
    - 系統應提供「預設自動提款通道」設定。
    - Risk 同意後，系統背景自動執行 Finance 鎖定並同意，不需人工操作。
    - **IF** 三方 API 建立提款單失敗 **OR** 回傳 `Reject`:
        - 狀態直接轉為 `Decline`。
        - **行為:** 為了與 T1 包網平台的簡便流程對齊，自動模式下若發生錯誤不退回人工處理。

---

**文件結束**
