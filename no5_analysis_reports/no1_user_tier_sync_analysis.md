# 會員階級與同步邏輯分析報告

## 目的

本報告旨在確認會員階級、資料同步權限、批次同步觸發時機，以及各角色間的互動邏輯。

---

## 會員階級定義

根據商業模式與使用者 Schema 定義，系統區分為以下階級：

### Tier 0, Local / Free
- **權限:** 僅限本地資料庫 WatermelonDB，無雲端同步功能。
- **功能:** 完整 CRUD 操作、基礎報表。
- **Entitlement:** 無，對應 `rc_entitlements` 為空或無 `premium` 鍵值。

### Tier 1, Cloud / Standard
- **權限:** 啟用 Sync Engine，支援雲端備份與多裝置同步。
- **功能:** 包含 Tier 0 所有功能，加上雲端同步。
- **Entitlement:** `premium`。

### Tier 2, Management / Pro 與 Tier 3, Intelligence / Ultra
- **權限:** 包含 Tier 1 所有同步權限。
- **功能:** 額外增加 Web Console 或 AI 功能。

---

## 資料同步權限與邏輯

### 權限判斷
- **檢查方式:** 透過 `isPremiumUser` 函式檢查 `user.rc_entitlements?.premium` 是否存在。

### 升級流程, Tier 0 to 1
- **觸發:** 監聽器偵測到 `premium` 權限生效。
- **行為:** 啟動 Sync Engine，強制執行 **Initial Sync**，即上傳本地所有資料並下載雲端資料。

### 降級流程, Tier 1 to 0
- **觸發:** 監聽器偵測到 `premium` 權限失效。
- **行為:** 執行 **Stop & Freeze** 策略。
    - 立即停止 Sync Engine。
    - 保留本地資料供離線使用。
    - 凍結雲端資料不再更新。

---

## 批次同步觸發機制

### 手動觸發, Manual
- **入口:** 使用者點擊 **立即同步** 按鈕。
- **檢查:**
    - 必須是 Premium 會員。
    - 必須通過冷卻時間，例如 5 分鐘。

### 自動觸發, Automatic
- **升級時:** 獲得權限當下自動觸發 Initial Sync。
- **每日檢查:** 規格中定義 `lastSyncCheckDate` 作為每日自動檢查點，暗示系統具備每日背景同步機制。

---

## 角色互動與檢查邏輯

### RevenueCat Server
- **職責:** 處理訂閱狀態變更。
- **行為:** 透過 Webhook 寫入 Firestore `users/{uid}` 的 `rc_entitlements` 欄位。

### Firestore
- **職責:** 儲存使用者權限狀態與同步資料。
- **行為:** 作為雲端資料來源與備份端點。

### App, User Management
- **職責:** 權限狀態管理。
- **行為:**
    - 監聽 `users/{uid}` 的 `onSnapshot`。
    - 當 `rc_entitlements` 變更時，即時更新本地 `PremiumContext`。

### App, Accounting
- **職責:** 執行同步與功能控制。
- **行為:**
    - 根據 `PremiumContext` 決定是否顯示或啟用 **立即同步** 按鈕。
    - 執行 Sync 時讀取 `updatedOn` 與 `lastSyncTimestamp` 進行增量同步。

---

## 潛在規格衝突

- **共用帳本 Shared Ledger:**
    - 產品定義文件中將其列為 **排除功能**。
    - 商業模式文件中 Tier 1 功能列表卻包含此項目。
    - **建議:** 若以產品定義為準，Tier 1 的核心價值應聚焦於 **個人雲端同步與備份**。

---

**文件結束**
---
