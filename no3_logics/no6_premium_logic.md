# Premium 邏輯規格: PremiumLogic

## 目的

- 提供從 IAP 平台更新本機訂閱狀態的入口
- 受限動作的授權判斷由 SubscriptionGateLogic 的 canUserPerformAction 處理

---

## refreshStatus 更新訂閱狀態

- **性質:**
  - 非同步執行，需處理網路錯誤
- **執行:**
  - 向 IAP 平台查詢當前帳號的有效購買紀錄
  - 解析購買清單，判斷是否包含有效 Premium 等級項目
  - 更新本機訂閱狀態
