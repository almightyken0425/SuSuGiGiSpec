# 登入畫面 (LoginScreen)

_(本文件定義登入畫面的 UI、流程與邏輯)_

## UI 佈局

- **視覺中心:** App Logo 或名稱 (例如 "速速記記")。
    
- **登入按鈕:** 一個醒目的「**使用 Google 登入**」按鈕 (包含 Google Logo 和文字)。
    
    
## 核心互動與流程


*   **App 啟動:** App 啟動時，`AppNavigator` (或 `AuthContext`) 檢查使用者是否已有有效的登入狀態 (例如，本地有 Firebase Auth 的 token)。
    
*   **判斷導航:**
    
    *   **若已登入:** 直接導航至 `HomeScreen`。
    *   
        *   `HomeScreen` 應**立刻**從「本機資料庫 (Local DB)」讀取資料並顯示 UI。
            
        *   所有「定期交易檢查」或「批次同步」任務均應在 `HomeScreen` 載入_之後_才**非同步**執行，絕不應阻塞 `HomeScreen` 的開啟。
        
    *   **若未登入:** 顯示此 `LoginScreen`。
        
*   **使用者點擊「使用 Google 登入」:**
    
    *   觸發 `authService.signInWithGoogle()` 函數。
        
*   **認證流程 (呼叫 `authService`):**
    
    *   App 呼叫 Firebase Authentication SDK，彈出 Google 帳號選擇視窗。
        
    *   使用者選擇帳號並同意授權。
        
*   **認證成功:**
    
    *   Firebase Auth 返回使用者憑證，`authService` 從中獲取 `userId` (Email)。
        
    *   `authService` 觸發「首次登入流程」：
        
        *   檢查 Firestore 該 `userId` 是否有資料。
            
        *   **新用戶:**
            
            *   **動作:** 在**本機資料庫 (Local DB)** 建立預設資料（基礎貨幣、時區、預設帳戶、預設類別 - 需符合免費版限制）。
                
            *   **注意:** **不執行**任何雲端上傳或同步。   
         
        *   **舊用戶:**
            
            *   **動作:** **不執行**任何操作。
                
            *   **注意:** 資料將在使用者升級為 Premium 並觸發「首次同步」（例如手動按「立即同步」）時才會從雲端下載。
            
    *   `AuthContext` 狀態更新為「已登入」。
        
*   **導航:** `AppNavigator` 偵測到登入狀態改變，自動導航至 `HomeScreen`。
    

## 錯誤處理

-   **使用者取消登入:** (例如關閉 Google 選擇視窗) - 停留在登入畫面，可選顯示一個非侵入性提示 (Toast) "登入已取消"。
    
-   **網路錯誤:** 登入過程中若無網路，應顯示錯誤提示 (例如 "請檢查網路連線")。
    
-   **認證失敗 (來自 Google/Firebase):** 顯示通用的錯誤提示 (例如 "登入失敗，請稍後再試")。