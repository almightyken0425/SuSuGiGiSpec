# 批次同步技術規格 (Batch Sync Spec)

_(本文件定義「本地優先」(Local-First) 架構下的付費版「批次同步」功能，此功能取代了原有的即時同步模型)_

## 核心架構 (Core Architecture)

- **架構模型:** 本地優先 (Local-First)。
    
    - **資料來源:** App 所有的讀取 (Read) 與寫入 (Write) 操作，**一律**針對「**本機資料庫 (Local DB)**」 (例如 SQLite 或 WatermelonDB)。
        
    - **UI 反應:** UI 應即時反應「本機資料庫」的變更。
        
- **雲端角色 (Firestore):**
    
    - Firestore 不再是即時資料來源，而是作為付費版使用者的「**被動備份與同步伺服器**」。
        
- **同步模型:**
    
    - 採用「**增量批次同步 (Delta Batch Sync)**」模型。
        
    - 僅同步自上次同步以來發生變更的資料。
        

## 資料結構先決條件 (Data Structure)

- **`updatedOn` (必要欄位):**
    
    - **要求:** **所有**需要同步的使用者資料表 (Accounts, Categories, Transactions, Transfers, Settings 等)，都**必須**包含 `updatedOn` (Unix Timestamp ms) 欄位。
        
    - **邏輯:**
        
        - **本機寫入時:** 任何「新增」或「修改」操作，都**必須**同時更新該筆紀錄的 `updatedOn` 為當前時間戳記。
            
        - **同步依據:** 此欄位是「增量同步」演算法的核心依據。
            
- **`deletedOn` (軟刪除):**
    

- **`lastSyncTimestamp` (本地儲存):**
    
    - **要求:** App 必須在裝置的本地儲存 (e.g., AsyncStorage) 中，持久化儲存一個 `lastSyncTimestamp` (Unix Timestamp ms) 變數。
        
    - **邏輯:** 這是「增量同步」的錨點。每次同步成功後，都必須更新此時間戳記。
        
- **`lastSyncCheckDate` (本地儲存 - 用於自動觸發):**
    
    - **要求:** App 必須在裝置的本地儲存 (e.g., AsyncStorage) 中，持久化儲存一個**日期標記** (例如 "2025-11-10")。
        
    - **邏輯:** 這是「每日自動觸發」的檢查點，與使用者的主要時區掛鉤。
        

## 衝突解決策略 (Conflict Resolution)

- **策略:** **最後寫入者獲勝 (Last Write Wins - LWW)**
    
    - **機制:** 此策略**隱含**在 `updatedOn` 欄位中。
        
    - **範例:**
        
        - 裝置 A (離線) 修改了 `Account-X` (`updatedOn: 10:05 AM`)。
            
        - 裝置 B (離線) 修改了_同一個_ `Account-X` (`updatedOn: 10:10 AM`)。
            
        - 裝置 B 先同步，將 `Account-X (10:10)` 上傳至雲端。
            
        - 裝置 A 後同步，上傳 `Account-X (10:05)`。
            
        - 裝置 A 接著下載，它會從雲端抓到 `Account-X (10:10)`（因為 `10:10` > 它的 `lastSyncTimestamp`）。
            
        - **最終結果:** 兩台裝置的 `Account-X` 都會是 `10:10` 的版本。`10:05` 的修改被_自動_覆蓋，達成了最終一致性。
            

## 同步觸發時機 (Sync Triggers)

### 自動觸發 (每日)

- **邏輯:** 這是付費版使用者的標準背景同步。
    
- **時機:** App 啟動時 (例如在「首頁畫面」的 `useEffect` 中)。
    
- **檢查:**
    
    - 檢查 `isPremiumUser` 是否為 `true`。
        
    - **檢查 `currentDateInUserTZ > lastSyncCheckDate`**（`currentDateInUserTZ` 是基於使用者「主要時區」的今天日期；`lastSyncCheckDate` 是上次執行自動同步的日期標記）。
        
- **動作:** 若上述條件皆滿足，則**非同步**執行 (不阻塞 UI)「批次同步流程」。
    

### 手動觸發

- **邏輯:** 允許使用者主動發起同步，此為**付費功能**。
    
- **入口:** 「設定 - 偏好設定」畫面中的「**立即同步 (Sync Now)**」按鈕。
    
- **檢查:**
    
    - **付費牆:** 點擊時，必須檢查 `isPremiumUser`。若為 `false`，導航至「付費牆畫面」並終止。
        
    - **冷卻機制 (防護):**
        
        - 點擊時，必須檢查 `Now < nextSyncAllowedTime` (儲存於本機的狀態)。
            
        - **若在冷卻期:** 顯示提示「您剛才同步過了，請 5 分鐘後再試」，並**終止**流程。
            
        - **若不在冷卻期:** 繼續執行。
            
- **動作:** **同步**執行 (顯示載入指示器)「批次同步流程」。
    

## 批次同步流程 (The Sync Process)

- **目標:** 執行雙向增量同步 (Two-Way Delta Sync)。
    
- **前提:** 取得當前的 `currentSyncTime = Now` (當次同步的時間戳記)。
    

### - 上傳階段 (Upload)

- **查詢 (本機):**
    
    - `find(all documents where updatedOn > lastSyncTimestamp)`
        
- **動作:**
    
    - 將所有查詢到的「本機變更」（包含新增、修改、軟刪除）批次上傳 (Batch Write) 至 Firestore。
        
    - **錯誤處理:** 若上傳失敗（例如網路中斷），**必須終止**整個流程，**不得**更新 `lastSyncTimestamp`。
        

### - 下載階段 (Download)

- **查詢 (雲端):**
    
    - `get(all documents from Firestore where updatedOn > lastSyncTimestamp AND userId == currentUserId)`
        
- **動作:**
    
    - 取得所有「雲端變更」的列表。
        
    - 遍歷列表，將每一筆資料批次寫入 (Batch Write)「本機資料庫」。
        
        - **Upsert 邏輯:** 依據 `id` 判斷，若本機已存在該 `id` 則「更新 (Update)」，若不存在則「插入 (Insert)」。
            
    - **錯誤處理:** 若下載或寫入本機失敗，**必須終止**整個流程，**不得**更新 `lastSyncTimestamp`。
        

### - 完成階段 (Finalize)

- **動作:**
    
    - 僅在「上傳」和「下載」**均**成功完成後，才執行此步驟。
        
    - **更新時間戳記:** 將裝置本地儲存的 `lastSyncTimestamp` 更新為 `currentSyncTime`。
        
    - **(針對自動觸發):** 如果此次同步是由「自動觸發」啟動的，則**必須**將 `lastSyncCheckDate` 更新為 `currentDateInUserTZ`（今天的日期標記）。
        
    - **(針對手動觸發):** 更新 `nextSyncAllowedTime = currentSyncTime + 5 分鐘`。
        
    - 隱藏載入指示器，顯示「同步成功」提示。
        

- **情境:** 付費版使用者登入一台新裝置（或剛升級為付費版並首次觸發同步）。
    
- **邏輯:**
    
    - 裝置本地的 `lastSyncTimestamp` 會是 `0` (或 `null`)。
        
- **流程:**
    
    - **上傳階段:**
        
        - 查詢 `updatedOn > 0`（即本機所有資料）。
            
        - 將本機所有資料上傳至 Firestore。
            
    - **下載階段:**
        
        - 查詢 `updatedOn > 0`（即雲端所有資料）。
            
        - 將雲端所有資料下載並寫入本機資料庫（LWW 策略會自動處理合併）。
            
    - **完成階段:** `lastSyncTimestamp` 被更新為當前時間。