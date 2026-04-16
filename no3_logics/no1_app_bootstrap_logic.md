# App 啟動流程: AppBootstrapFlow

---

## bootstrapApp 啟動 App

- 確認 Firebase Auth 狀態，並依登入結果調度背景任務
- **執行:**
  - 讀取本地快取的 Firebase Auth 狀態
  - **IF** 已登入:
    - 呼叫 runCoreBackgroundTasks，於背景執行核心維護任務
    - 查詢本地快取的 Premium 權限狀態
    - **IF** Premium 權限有效:
      - 呼叫 runPremiumBackgroundTasks，於背景執行付費者同步任務

---

## runCoreBackgroundTasks 執行核心背景任務

- 刷新 Premium 到期狀態，並依日期條件補產生定期交易
- **性質:**
  - 非同步，不阻塞主流程
- **Premium 狀態更新:**
  - **執行:**
    - 向 IAP 服務查詢最新購買憑證，更新本地 Premium 到期狀態
- **定期交易補產生:**
  - **條件:**
    - 以使用者時區計算的當前日期晚於上次定期交易檢查日
  - **執行:**
    - 依 Schedules 表的排程設定，補產生所有尚未建立的 Transactions 與 Transfers 紀錄
    - 更新上次定期交易檢查日為當前日期

---

## runPremiumBackgroundTasks 執行付費者背景任務

- 依日期條件觸發批次雲端同步
- **性質:**
  - 非同步，不阻塞主流程
- **批次同步自動觸發:**
  - **條件:**
    - 計算的現在時間晚於上次同步時間
  - **執行:**
    - 觸發批次同步流程
    - 更新上次同步時間為當前時間
