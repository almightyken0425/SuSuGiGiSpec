# 使用分析同意提示: UsageAnalyticsConsentPrompt

## 畫面目標

- 首次啟動取得使用分析同意

---

## 觸發情境

- 偏好設定已完成載入
- 使用分析尚未選擇

---

## 佈局

### 確認對話框

- 標題為協助改善
- 訊息為分享功能使用情況
- 訊息為不含記帳內容
- 不要分享 按鈕
- 同意並繼續 按鈕

---

## 互動

- **點按不要分享:**
  - 委派 setUsageAnalyticsConsent
  - 目標同意狀態為 false
  - 關閉對話框

- **點按同意並繼續:**
  - 委派 setUsageAnalyticsConsent
  - 目標同意狀態為 true
  - 關閉對話框
