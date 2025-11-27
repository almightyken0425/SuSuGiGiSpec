# 登入流程矛盾分析報告

> **日期**: 2025-11-27
> **主題**: 全域互動總覽 vs. 首次登入邏輯之矛盾分析

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

## 5. 補充分析：登入時機與使用者體驗 (UX)

針對「是否應強制 T0 使用者登入」的進一步分析：

### 5.1 技術層面：T0 是否需要 User Record？

*   **結論**: **不需要**。
*   **原因**:
    *   **權限判斷在 Client**: App 透過 RevenueCat SDK 直接與 Store 溝通，T0 狀態由本地 SDK 判斷，無需 Firestore 介入。
    *   **Webhook 依賴性**: Webhook 僅用於通知後端開啟 Sync 權限。T0 不需 Sync，因此後端無資料也無妨。
    *   **資料一致性**: 當使用者決定付費 (變為 T1) 時，App 會強制要求登入，此時再建立 User Record 即可完美銜接。

### 5.2 體驗層面：早登入 (Early) vs. 晚登入 (Contextual)

| 比較項目 | 情境 A：強制早登入 (Early Login) | 情境 B：情境式晚登入 (Contextual Login) |
| :--- | :--- | :--- |
| **流程** | 下載 -> **阻擋 (登入)** -> 首頁 -> 付費 | 下載 -> **直接使用 (Guest)** -> 付費/備份 -> **登入** |
| **優點** | 資料歸戶明確，行銷追蹤容易。 | **無縫體驗**，降低進入門檻，符合 Local-First 精神。 |
| **缺點** | **流失率高**，使用者未體驗價值即被阻擋；T0 登入後無備份功能，易產生困惑。 | 需處理「本地資料 -> 雲端帳號」的資料轉移 (Onboarding) 邏輯。 |
| **結論** | **不推薦** | **強烈推薦** |

### 5.3 建議流程 (Ideal Flow)

1.  **首次啟動**: **不登入**，直接進入 App (Guest Mode, T0)。
2.  **日常使用**: 資料存於本地 WatermelonDB。
3.  **觸發點**: 使用者點擊「訂閱 Premium」或「手動備份」。
4.  **登入引導**: 提示「為了確保雲端權益，請先登入」。
5.  **執行登入**: 登入後，將本地資料綁定至該帳號。
6.  **完成訂閱**: RevenueCat 通知後端，開啟 Sync Engine。

## 6. 決策記錄 (Decision Record)

> **日期**: 2025-11-27
> **決策者**: User & AI

1.  **情境式登入 (Contextual Login)**:
    *   **決策**: 採納 **Local-First** 策略，App 啟動時不強制登入。僅在「付費」或「手動備份」等關鍵時刻要求登入。
    *   **理由**: 強制登入就像「走進店家連東西都還沒看就要求辦會員」，體驗極差。應在「結帳櫃台」(付費/備份) 才詢問會員意願。

2.  **不實作主動登出 (No Explicit Logout)**:
    *   **決策**: App 不提供主動登出按鈕。
    *   **理由**: 除非發生非自主選擇的極端狀況 (如 Token 失效、帳號被刪除、App 資料被清除)，否則保持登入狀態。
    *   **例外**:
        *   Refresh Token 失效 (密碼修改、帳號停用、後台撤銷)。
        *   App 資料/快取被清除。
        *   Firebase 專案設定變更。

3.  **離線漏洞容忍 (Offline Loophole Tolerance)**:
    *   **決策**: **定期交易 (Recurring Transactions)** 改為在 App 啟動時依據 **本地資料** 執行。
    *   **理由**:
        *   **保障離線可用性**: 不希望使用者因為沒連網就無法執行定期交易。
        *   **接受 Trade-off**: 即使使用者訂閱過期但尚未連網同步權限，App 仍會繼續產生定期交易。
        *   **風險評估**: 相信極少數使用者會為了省小錢而刻意每次記帳都斷網，此風險可接受。

