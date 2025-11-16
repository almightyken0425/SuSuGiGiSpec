## App 啟動檢查流程

- **觸發:** App 啟動且使用者已登入時 (由 LoginScreen 或 AppNavigator 觸發)
- **目的:** 依序執行所有必要的背景啟動任務
- **流程:**
    - **非同步執行:**
        - **執行:** 定期交易檢查
        - **檢查:** `currentDateInUserTZ > lastRecurringCheckDate`
        - **IF True:**
            - **執行:** 補產生邏輯
            - **更新:** `lastRecurringCheckDate`
        - **完成後, 執行:** 批次同步自動觸發
        - **檢查:**
            - `PremiumContext.isPremiumUser`
            - `currentDateInUserTZ > lastSyncCheckDate`
        - **IF** 兩者皆 True:
            - **執行:** 批次同步流程
            - **更新:** `lastSyncCheckDate`