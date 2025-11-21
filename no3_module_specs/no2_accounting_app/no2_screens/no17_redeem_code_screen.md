# 序號兌換畫面 (Redeem Code Screen)

## 1. 畫面摘要
- **名稱**: RedeemCodeScreen
- **路徑**: `/settings/redeem`
- **功能**: 讓使用者輸入序號以兌換權益 (會員升級、展期等)。

## 2. UI 結構

### 2.1 Header
- **Title**: "兌換序號"
- **Left**: Back Button (返回 PreferenceScreen)

### 2.2 輸入區域 (Input Section)
- **TextField**:
  - **Placeholder**: "請輸入 12 位數序號"
  - **Format**: 自動格式化為 `XXXX-XXXX-XXXX` (每 4 碼加 Dash)
  - **Keyboard**: ASCII Capable / Uppercase
- **Helper Text**: "序號位於您的實體卡片背面或活動信件中"

### 2.3 操作按鈕 (Action)
- **Button**: "立即兌換"
  - **State**:
    - Disabled: 當輸入長度不足 12 碼時。
    - Loading: 當 API 請求中。

### 2.4 歷史記錄 (History Section) - Optional
- **Title**: "最近兌換記錄"
- **List**: 顯示最近 5 筆兌換記錄 (日期 + 項目)。

## 3. 互動邏輯

### 3.1 輸入驗證
- **即時格式化**: 輸入時自動轉大寫，並插入分隔線。
- **長度檢查**: 限制最大長度為 14 (12字元 + 2分隔線)。

### 3.2 兌換流程
1. **點擊兌換**:
   - 顯示 Loading Spinner。
   - 呼叫 `POST /api/v1/redeem`。
2. **成功 (Success)**:
   - 隱藏 Loading。
   - 顯示 Success Dialog / BottomSheet:
     - Title: "兌換成功！"
     - Content: "您已升級為 Tier 1 會員，效期至 2024/12/31"
     - Action: "確定" (點擊後返回上一頁或重整 User Profile)。
3. **失敗 (Error)**:
   - 隱藏 Loading。
   - 顯示 Error Message (Toast or Inline Error):
     - "序號無效或已過期 (CODE_EXPIRED)"

## 4. 導航
- **Back**: 返回上一頁。
- **Success**: 通常返回上一頁，並觸發 App 狀態更新 (Refetch User Profile)。
