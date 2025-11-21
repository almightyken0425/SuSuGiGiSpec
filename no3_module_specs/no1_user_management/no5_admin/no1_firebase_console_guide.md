# Firebase Console 操作手冊 (Firebase Console Guide)

## 1. 前置準備

### 1.1 存取權限
- **角色**: 需具備 `Firebase Editor` 或 `Cloud Datastore User` 權限。
- **帳號**: 僅限授權的營運團隊成員帳號。

### 1.2 環境確認
- **網址**: [Firebase Console](https://console.firebase.google.com/)
- **專案**: 確認左上角選擇正確的專案 (Dev / Staging / Prod)。

## 2. 手動生成序號步驟

### 2.1 進入資料庫
1. 點擊左側選單 **Build** > **Firestore Database**。
2. 在 Data 分頁中，找到集合 (Collection) `RedeemCodes`。

### 2.2 新增序號文件
1. 點擊 `RedeemCodes` 欄位上方的 **+ Add document**。
2. **Document ID**: 點擊 **Auto-ID** 自動生成。
3. **Field 填寫**:
   - `code` (string): 輸入唯一序號 (e.g., `VIP-2024-001`)。
   - `codeType` (string): 輸入類型 (e.g., `tier_upgrade`)。
   - `targetTier` (number): 輸入目標 Tier (e.g., `1`)。
   - `durationDays` (number): 輸入天數 (e.g., `30`)。
   - `maxRedemptions` (number): 輸入次數 (e.g., `1`)。
   - `currentRedemptions` (number): 輸入 `0`。
   - `isActive` (boolean): 選擇 `true`。
   - `createdBy` (string): 輸入您的 Email。
   - `createdOn` (number): 輸入當前 Timestamp (可搜尋 "current timestamp" 取得)。
   - `updatedOn` (number): 同上。

4. 點擊 **Save** 儲存。

## 3. 查詢與管理

### 3.1 篩選序號
- 使用 Firestore 的 **Filter** 功能。
- 例如: `Where code == "VIP-2024-001"`。

### 3.2 停用序號
1. 找到該序號文件。
2. 將 `isActive` 欄位改為 `false`。
3. 點擊 **Update**。

### 3.3 查看兌換狀況
- 觀察 `currentRedemptions` 欄位數值。
