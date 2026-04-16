# 登出邏輯: LogoutLogic

## logout 登出

- **執行:**
  - 清除本地 Premium 快取狀態
  - 歸零每日 Firestore 讀寫計數
  - 保留本地帳務資料，不執行清除
  - 觸發 Firebase Auth 登出，清除本地登入憑證
  - 重置 lastRecurringCheckDate 與 lastSyncCheckDate

---

## handleReLogin 處理重新登入

- **性質:**
  - 非同步，需處理網路錯誤
- **執行:**
  - **IF** 與本地快取帳號相同:
    - 讀取 Firestore 偏好設定，以雲端設定覆蓋本地設定
    - 觸發批次同步流程
  - **ELSE:**
    - 通知使用者本地存有其他帳號資料，依其選擇保留或清除後繼續
