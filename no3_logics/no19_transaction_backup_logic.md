# 交易備份邏輯: TransactionBackupLogic

## 目的

- CloudSync 與 TransactionBackup 軌的承載點
- 將 transactions、transfers、accounts、categories、currency_rates、schedules 上傳至 Firestore users/{uid}/{collection}
- 全 user 寫入，含 LEVEL_0，不受 analyticsConsent 影響
- 法律基礎為 Contract，履行記帳服務契約所必要
- 單向上傳，無 user 端取回介面
- 不使用 Firestore Real-time listener
- 觸發來源為 AppBootstrapLogic 的 runCoreBackgroundTasks 與 LoginLogoutLogic 的 handleReLogin
- 冷卻時間戳屬裝置層級持久化，跨 App 重啟與使用者切換不重置
- lastSyncedAt 屬 per-user 的 Delta watermark
- 冷卻時間戳與 lastSyncedAt 兩種儲存層級不混用

---

## runBackup 執行備份

- 軌道入口，承載原批次同步協調職責

- **性質:**
  - 非同步執行
  - 需處理網路錯誤與 Firestore 配額錯誤
- **執行:**
  - **IF** 帳號刪除進行中:
    - RETURN；上傳與伺服器刪除交錯會把資料寫回成雲端孤兒，詳見 DeleteUserAccountLogic
  - **IF** 當前無登入使用者:
    - RETURN
  - **IF** 備份已在進行中:
    - RETURN
  - **IF** 距上次備份起始時間未滿 5 分鐘冷卻:
    - RETURN
  - **ELSE:**
    - 標記備份進行中旗標
    - 記錄本次備份起始時間至裝置層級持久化儲存
    - 委派至 QuotaManagementLogic 的 checkQuota，讀取寫入允許旗標
    - **IF** 寫入禁止:
      - 跳過本次上傳，等下次 UTC+0 跨日重置
    - **ELSE:**
      - 探測 Firestore 端是否存在此 user 資料
        - 探測方式：查遠端 transactions 集合，最多取 1 筆，非空即視為遠端已有資料
        - 以單一集合近似判定，不遍歷其餘集合
        - 探測失敗：保守視為遠端無資料，續走 runInitialBackup
      - **IF** 遠端無資料:
        - 委派至 runInitialBackup
      - **ELSE:**
        - 委派至 runDeltaBackup
    - 解除備份進行中旗標
- **遠端有資料但 lastSyncedAt 為 Null:**
  - **行為:**
    - 視為全量 Delta，走 runDeltaBackup，不另走 runInitialBackup
  - **理由:**
    - 上傳採 upsert 冪等，全量重傳安全，無須區分初次或增量

---

## runInitialBackup 執行初次完整上傳

- 一次性全量上傳六個 collections

- **性質:**
  - 非同步，需處理網路錯誤與 Firestore 配額錯誤
- **執行:**
  - 讀取本機所有 transactions、transfers、accounts、categories、currency_rates、schedules
  - 依集合分批寫入 Firestore users/{uid}/{collection}，每批 500 筆
  - 委派至 QuotaManagementLogic 的 incrementQuota，累計上傳筆數至當日寫入配額
  - 寫入完成後更新 Settings 表 lastSyncedAt 為當下時間

---

## runDeltaBackup 執行增量上傳

- 以 lastSyncedAt 為基準上傳變更

- **性質:**
  - 非同步，需處理網路錯誤與 Firestore 配額錯誤
- **執行:**
  - 以 Settings 表 lastSyncedAt 為 Delta 篩選基準，讀取自上次完成同步後的變更，涵蓋 transactions、transfers、accounts、categories、currency_rates、schedules
  - **IF** 無任何變更:
    - 跳過上傳，不更新 lastSyncedAt，RETURN
  - **ELSE:**
    - 依集合分批寫入 Firestore users/{uid}/{collection}，每批 500 筆
    - 委派至 QuotaManagementLogic 的 incrementQuota，累計上傳筆數至當日寫入配額
    - 寫入完成後更新 Settings 表 lastSyncedAt 為當下時間
