# 登入流程矛盾分析報告

> **日期**: 2025-11-27
> **主題**: 全域互動總覽 vs. 首次登入邏輯之矛盾分析
> **狀態**: 待確認

## 1. 問題描述

在比對 `no1_interaction_flow.md` (全域互動總覽) 與 `no2_first_login_flow.md` (首次登入邏輯) 後，發現兩者在 **「使用者資料建立 (User Creation)」** 的核心邏輯上存在根本性的矛盾。

## 2. 矛盾點分析

| 比較維度 | `no1_interaction_flow.md` (總覽) | `no2_first_login_flow.md` (詳細邏輯) |
| :--- | :--- | :--- |
| **核心架構** | **Cloud-First (雲端優先)** | **Local-First (本地優先)** |
| **資料建立時機** | 登入後 **立即** 連線 Firestore 建立 User Profile。 | 登入後 **優先** 在 WatermelonDB 建立/更新使用者記錄。 |
| **強健性機制** | 使用 `Loop 3 Times` 重試機制，確保雲端 Profile 建立成功。 | 依賴本地 DB 的原子性操作 (Atomic Upsert)，確保本地資料一定存在。 |
| **Tier 0 行為** | 未區分，暗示所有使用者皆需建立雲端 Profile。 | **明確區分**：Tier 0 使用者 **不啟動 Sync Engine**，完全不連線 Firestore。 |
| **寫入操作** | 直接呼叫 Firestore API (`App->>Cloud`). | 禁止直接寫入，改由 Sync Engine 負責 (若有權限)。 |

## 3. 影響評估

若依照 `no1_interaction_flow.md` (總覽) 實作：
1.  **違反 Local-First 原則**: 強制依賴網路才能完成登入流程。
2.  **增加成本**: Tier 0 免費使用者也會消耗 Firestore 寫入額度。
3.  **體驗不一致**: 離線登入將會失敗 (因為無法建立雲端 Profile)，與「離線可用」承諾相違背。

## 4. 建議解決方案

**採用 `no2_first_login_flow.md` 的 Local-First 邏輯為準。**

### 具體修改建議 (針對總覽文件)

1.  **移除** `App->>Cloud: 查詢/建立 User Profile` 的迴圈邏輯。
2.  **新增** `App->>Local: Ensure Local User` 的步驟。
3.  **調整** Sync Engine 啟動條件：
    *   僅在 `isPremium == true` 時啟動。
    *   由 Sync Engine 負責後續的雲端 Profile 同步 (若不存在則由 Sync Engine 上傳建立)。

### 修正後的虛擬流程

```mermaid
sequenceDiagram
    U->>App: Google Sign-In
    App->>Auth: 取得 User
    
    rect rgb(240, 255, 240)
        Note right of App: Local-First 處理
        App->>Local: Upsert User Record (WatermelonDB)
        Local-->>App: OK
    end
    
    App->>RC: 檢查權限
    
    alt isPremium
        App->>Sync: 啟動 Sync Engine
        Note right of Sync: 由 Sync Engine 負責雲端資料建立與同步
    else isFree
        App->>Sync: 確保 Sync Engine 關閉
    end
```
