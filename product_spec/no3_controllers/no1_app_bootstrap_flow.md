# App 啟動流程

## 流程

- **觸發:** 使用者開啟 App
- **行為:** 顯示 Splash 啟動畫面
- **行為:** 檢查 本機儲存的 Auth State 認證狀態
- **IF** 認證狀態 == `Valid` 已登入
    - **導航:** HomeScreen
    - **行為:** 於 HomeScreen 立即從 本機 DB 讀取資料並顯示 UI
    - **IF** `PremiumContext.isPremiumUser` == True
        - **目的:** 依序執行所有必要的付費者背景啟動任務
        - **非同步執行:**
            - **執行:** 定期交易檢查
            - **檢查:** `currentDateInUserTZ > lastRecurringCheckDate`
            - **IF True:**
                - **執行:** 補產生邏輯
                - **更新:** `lastRecurringCheckDate`
            - **完成後, 執行:** 批次同步自動觸發
            - **檢查:** `currentDateInUserTZ > lastSyncCheckDate`
            - **IF True:**
                - **執行:** 批次同步流程
                - **更新:** `lastSyncCheckDate`
- **IF** 認證狀態 == `null` 未登入
    - **導航:** LoginScreen