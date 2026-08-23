# 使用行為分析: UsageAnalyticsLogic

## 目的

- 蒐集正式版核心流程事件
- 同意前不蒐集事件
- 事件不帶任何參數
- 不設定 Analytics User ID
- 自訂事件不含記帳內容
- 不啟用廣告用途
- 啟用後接受平台生命週期與購買自動事件

---

## configureUsageAnalytics 設定使用分析

- **輸入:**
  - 使用行為分析同意狀態
- **執行:**
  - 廣告儲存保持拒絕
  - 廣告使用者資料保持拒絕
  - 廣告個人化保持拒絕
  - **IF** 同意狀態為 false:
    - 分析儲存設為拒絕
    - 停用 Analytics 蒐集
  - **ELSE:**
    - 分析儲存設為允許
    - 啟用 Analytics 蒐集

---

## recordFirstEntryStarted 記錄首次記帳開始

- **執行:**
  - 查詢活躍交易數量
  - **IF** 數量為零:
    - 記錄 `first_entry_started`

---

## recordFirstEntryCompleted 記錄首次記帳完成

- **執行:**
  - 查詢活躍交易數量
  - **IF** 數量為一:
    - 記錄 `first_entry_completed`

---

## recordRecurringCreated 記錄定期交易建立

- **執行:**
  - 記錄 `recurring_created`

---

## recordExportUsed 記錄資料匯出

- **執行:**
  - 記錄 `export_used`

---

## recordPaywallViewed 記錄付費牆顯示

- **執行:**
  - 記錄 `paywall_viewed`
