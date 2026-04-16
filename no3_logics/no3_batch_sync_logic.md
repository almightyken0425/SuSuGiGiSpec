# 批次同步邏輯: BatchSyncLogic

## triggerManualSync 手動觸發批次同步

- 付費用戶手動發起批次同步，含 Premium 驗證與冷卻機制
- **執行:**
  - 查詢本地 Premium 權限狀態
  - **IF** Premium 無效:
    - 終止流程
  - **IF** 當前時間早於下次允許同步時間:
    - 終止流程
  - 呼叫 runBatchSync
  - **IF** 同步成功:
    - 更新下次允許同步時間為當前時間加 5 分鐘

---

## runBatchSync 執行批次同步

- 雙向增量同步，上傳本機變更並下載雲端更新，以 Last Write Wins 合併衝突
- **執行:**
  - 記錄當前時間為本次同步時間
  - **上傳階段:**
    - **執行:**
      - **IF** 本機 Settings 的 updatedOn 晚於上次同步時間:
        - 將本機偏好設定推送至 Firestore `users/{uid}`
      - 查詢本機所有 updatedOn 晚於上次同步時間的資料
      - 批次上傳至 Firestore
  - **IF** 上傳失敗:
    - **回傳:** 
      - 失敗
  - **下載階段:**
    - **執行:**
      - 從 Firestore `users/{uid}` 取得偏好設定
      - **IF** 雲端 updatedAt 晚於本機 Settings 的 updatedOn:
        - 將雲端偏好覆寫至本機 Settings 表
      - 查詢 Firestore 所有 updatedOn 晚於上次同步時間且屬於當前用戶的資料
      - 批次寫入至本機資料庫
        - **IF** 本機已存在相同 id: 更新
        - **IF** 本機不存在相同 id: 插入
  - **IF** 下載或寫入失敗:
    - **回傳:** 失敗
  - **完成階段:**
    - **執行:**
      - 更新上次同步時間為本次同步時間
  - **回傳:** 成功

---

## handlePremiumUpgrade 處理付費升級

- 用戶升級付費版後強制執行全量同步，建立初始同步錨點
- **執行:**
  - 重設上次同步時間為 0
  - 呼叫 runBatchSync

---

## handlePremiumExpiry 處理付費到期

- 訂閱到期後停止所有背景同步排程，保留本機資料
- **執行:**
  - 終止所有背景同步排程
  - 保留本機資料庫資料，不執行任何刪除
