# 序號驗證邏輯 (Redeem Code Validation Logic)

## 1. 邏輯摘要
- **名稱**: RedeemCodeValidation
- **目的**: 驗證使用者輸入的序號是否有效，並執行兌換後的權益更新。

## 2. 驗證流程 (Validation Flow)

### 2.1 前端預檢查 (Client-Side)
- **觸發**: 使用者輸入序號時或點擊兌換按鈕。
- **檢查**:
  - 格式是否符合 `XXXX-XXXX-XXXX`。
  - 是否包含非法字元。
- **結果**: 若不符，直接顯示錯誤，不送出請求。

### 2.2 後端驗證 (Server-Side)
- **觸發**: 呼叫 `redeemCode` API。
- **步驟**:
  1. **查詢序號**: 根據 `code` 查詢 `RedeemCodes` 表。
     - 若無此序號 -> Return `CODE_NOT_FOUND`
  2. **檢查狀態**:
     - `isActive` == false -> Return `CODE_INACTIVE`
     - `expiresOn` < Now -> Return `CODE_EXPIRED`
     - `currentRedemptions` >= `maxRedemptions` -> Return `CODE_DEPLETED`
  3. **檢查重複兌換**:
     - 查詢 `RedemptionHistory` 是否已有 (userId, codeId) 的記錄。
     - 若有 -> Return `ALREADY_REDEEMED`

## 3. 兌換執行 (Execution)

若驗證通過，執行以下交易 (Transaction)：

1. **更新序號狀態**:
   - `RedeemCodes.currentRedemptions` + 1
2. **記錄兌換歷史**:
   - 新增 `RedemptionHistory` 記錄。
3. **更新使用者權益**:
   - **Tier Upgrade**: 更新 `Users.userTier`。
   - **Subscription Extension**: 更新 `Users.subscriptionEndDate`。
     - 若原已是會員，展期 (原到期日 + durationDays)。
     - 若非會員，新購 (Now + durationDays)。
4. **回傳結果**:
   - Success Message
   - Updated User Profile

## 4. 錯誤代碼表

| Code | Message |
|------|---------|
| `INVALID_FORMAT` | 序號格式錯誤 |
| `CODE_NOT_FOUND` | 序號不存在 |
| `CODE_INACTIVE` | 序號未啟用 |
| `CODE_EXPIRED` | 序號已過期 |
| `CODE_DEPLETED` | 序號已被兌換完畢 |
| `ALREADY_REDEEMED` | 您已兌換過此序號 |
