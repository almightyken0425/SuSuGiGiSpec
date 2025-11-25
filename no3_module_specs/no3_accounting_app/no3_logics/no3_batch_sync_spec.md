# 批次同步規格: BatchSyncSpec

## 核心架構

> [!NOTE]
> 完整同步流程圖請參閱: `no1_interaction_flows/no2_accounting_flows.md`

- **架構模型:** 本地優先, Local-First
    - **資料來源:** App 讀寫操作, 一律針對 本機資料庫 Local DB
    - **UI 反應:** UI 即時反應 本機資料庫
- **雲端角色: Firestore**
    - **定位:** 付費版 被動備份與同步伺服器
- **同步模型:**
    - **名稱:** 增量批次同步, Delta Batch Sync
    - **行為:** 僅同步 增量資料

---

## 資料結構先決條件

- **updatedOn: 必要欄位**
    - **要求:** 所有需同步資料表, 必須包含 updatedOn
    - **邏輯:**
        - **本機寫入:** 新增 或 修改 操作, 必須更新 updatedOn
        - **同步依據:** updatedOn
- **deletedOn: 軟刪除**
- **lastSyncTimestamp: 本地儲存**
    - **要求:** 本地持久化儲存 lastSyncTimestamp
    - **邏輯:** 增量同步錨點, 同步成功後更新
- **lastSyncCheckDate: 本地儲存**
    - **要求:** 本地持久化儲存 日期標記
    - **邏輯:** 每日自動觸發檢查點, 與使用者主要時區掛鉤

---

## 衝突解決策略

- **策略:** 最後寫入者獲勝, Last Write Wins, LWW
- **機制:** 依據 updatedOn
- **範例:**
    - 裝置 A 離線修改 Account-X, updatedOn: 10:05 AM
    - 裝置 B 離線修改 Account-X, updatedOn: 10:10 AM
    - 裝置 B 先同步, 上傳 10:10 版本
    - 裝置 A 後同步, 上傳 10:05 版本
    - 裝置 A 接著下載, 抓到 10:10 版本
    - **最終結果:** 兩台裝置皆為 10:10 版本, 10:05 修改被覆蓋

---

## 同步觸發時機

- **手動觸發: 付費功能**
    - **入口:** 設定 -> 偏好設定 -> 立即同步 按鈕
    - **檢查: Premium**
        - `PremiumContext.isPremiumUser`
        - **IF False:**
            - **導航:** PaywallScreen
            - **終止:** 流程
    - **檢查: 冷卻機制**
        - `Now < nextSyncAllowedTime`
        - **IF True:**
            - **提示:** 您剛才同步過了, 請 5 分鐘後再試
            - **終止:** 流程
    - **行為:**
        - 同步執行 批次同步流程
        - 顯示載入指示器

---

## 批次同步流程

- **目標:** 雙向增量同步, Two-Way Delta Sync
- **前提:** currentSyncTime = Now
- **上傳階段: Upload**
    - **查詢: 本機**
        - `find(all documents where updatedOn > lastSyncTimestamp)`
    - **行為:** 批次上傳 本機變更 至 Firestore
    - **錯誤處理:**
        - **IF** 上傳失敗:
            - **終止:** 流程
            - **禁止:** 更新 lastSyncTimestamp
- **下載階段: Download**
    - **查詢: 雲端**
        - `get(all documents from Firestore where updatedOn > lastSyncTimestamp AND userId == currentUserId)`
    - **行為:**
        - 取得 雲端變更 列表
        - 批次寫入 雲端變更 至 本機資料庫
    - **Upsert 邏輯:**
        - **依據:** id
        - **IF** 本機已存在: 更新 Update
        - **IF** 本機不存在: 插入 Insert
    - **錯誤處理:**
        - **IF** 下載或寫入本機失敗:
            - **終止:** 流程
            - **禁止:** 更新 lastSyncTimestamp
- **完成階段: Finalize**
    - **條件:** 上傳 與 下載 均成功
    - **行為:**
        - **更新:** 本地 `lastSyncTimestamp` 為 `currentSyncTime`
        - **更新: 手動觸發**
            - `nextSyncAllowedTime = currentSyncTime + 5 分鐘`
        - **提示:**
            - 隱藏載入指示器
            - 顯示 同步成功

---

## 首次同步流程

- **情境:**
    - 付費版使用者登入新裝置
    - 剛升級付費版並首次觸發同步
- **邏輯:** `lastSyncTimestamp` 為 0 或 null
- **流程:**
    - **上傳階段:**
        - **查詢:** `updatedOn > 0`
        - **行為:** 上傳 本機所有資料
    - **下載階段:**
        - **查詢:** `updatedOn > 0`
        - **行為:** 下載 雲端所有資料 寫入本機
        - **備註:** LWW 策略自動合併
    - **完成階段:**
        - `lastSyncTimestamp` 更新為當前時間