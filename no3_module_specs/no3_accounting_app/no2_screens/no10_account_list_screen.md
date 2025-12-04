# 帳戶列表畫面: AccountListScreen

## 畫面目標

- **提供:** 查看、排序、管理所有帳戶的介面
- **作為:** 新增、編輯、停用、刪除特定帳戶的入口

```text
+--------------------------------+
| < Back      Accounts     Merge |
+--------------------------------+
| My Accounts        [+ Add]     |
| [Icon] Account Name      [=]   |
|        Type                    |
| [Icon] Account Name      [=]   |
|        Type                    |
|                                |
|                                |
+--------------------------------+

Left Swipe Revealed:
+--------------------------------+
| [Icon] Account N [停用] [刪除] |
+--------------------------------+
```

---

## UI 佈局

- **頂部導航列:**
    - `返回按鈕`
        - **導航:** SettingsScreen
    - `標題` 帳戶管理
    - `合併按鈕`
        - **導航:** MergeEditorScreen
        - **參數:** mode = Account
- **帳戶區:**
    - **區塊標題:**
        - `標題` 我的帳戶
        - `新增按鈕`
            - **觸發:** 付費牆檢查
            - **導航:** AccountEditorScreen
    - **帳戶列表:**
        - **UI:** DraggableFlatList
        - **排序:** 依 `sortOrder` 排序
        - **空狀態:** 您尚未建立任何帳戶
        - **列表項目:**
            - `圖示`
            - `名稱`
            - `帳戶類型`
            - `拖拉圖示`
            - **視覺標示停用:**
                - **條件:** `disabledOn` 非 null
                - **UI:** 灰色文字
            - **左滑操作** (Trailing Swipe Actions):
                - `停用/啟用按鈕`
                    - **標題:**
                        - IF 當前為啟用狀態: 停用
                        - IF 當前為停用狀態: 啟用
                    - **顏色:** 橘色背景
                - `刪除按鈕`
                    - **標題:** 刪除
                    - **顏色:** 紅色背景

---

## 核心邏輯

- **資料載入:**
    - **觸發:** 畫面載入
    - **來源:** 本機 DB
    - **查詢:** 所有 `Accounts`
    - **過濾:** `deletedOn` 為 null
    - **排序:** 依 `sortOrder` 初始排序
- **互動:**
    - **點擊項目:**
        - **導航:** AccountEditorScreen
        - **模式:** 編輯
        - **參數:** accountId
    - **拖拉排序:**
        - **行為:** 更新受影響帳戶的 `sortOrder`
        - **儲存:** 寫入本機 DB
        - **欄位:** 必須更新所有受影響帳戶的 `updatedOn`
    - **點擊新增:**
        - **導航:** AccountEditorScreen
        - **模式:** 新增
    - **點擊合併:**
        - **導航:** MergeEditorScreen
        - **參數:** mode = Account
- **左滑操作:**
    - **停用/啟用切換:**
        - **觸發:** 點擊停用/啟用按鈕
        - **行為:** 顯示確認 Alert
        - **Alert 內容:**
            - **標題:**
                - IF 當前為啟用: 確認停用
                - IF 當前為停用: 確認啟用
            - **訊息:**
                - IF 停用: "停用後此帳戶將不會出現在選擇列表中"
                - IF 啟用: "啟用後此帳戶將重新出現在選擇列表中"
            - **按鈕:** 取消、確認
        - **確認後:**
            - **IF 當前為啟用:** 設定 `disabledOn` 為當前時間戳記
            - **IF 當前為停用:** 設定 `disabledOn` 為 null
            - **更新:** `updatedOn` 欄位
            - **UI:** 列表自動重新整理，更新視覺標示
    - **刪除操作:**
        - **觸發:** 點擊刪除按鈕
        - **行為:** 顯示確認 Alert
        - **Alert 內容:**
            - **標題:** 確認刪除
            - **訊息:** "刪除此帳戶將一併刪除所有相關的交易與轉帳紀錄，此動作無法復原。"
            - **按鈕:** 取消（預設）、刪除（破壞性樣式）
        - **確認後:**
            - **軟刪除帳戶:** 設定本機 DB 該筆 `Account` 的 `deletedOn` 欄位
            - **連動刪除交易:** 搜尋所有 `accountId` 為此帳戶的 `Transactions` 並設定 `deletedOn`
            - **連動刪除轉帳:** 搜尋所有 `fromAccountId` 或 `toAccountId` 為此帳戶的 `Transfers` 並設定 `deletedOn`
            - **更新時間:** 所有受影響資料皆需更新 `updatedOn`
            - **UI:** 從列表中移除該項目
- **付費牆檢查:**
    - **觸發:** 點擊新增按鈕
    - **檢查:**
        - `PremiumLogic.checkPremiumStatus()` 狀態
        - 本機 DB 帳戶總數
    - **IF 免費版 AND 帳戶數量已達上限:**
        - **導航:** PaywallScreen
    - **ELSE:**
        - **導航:** AccountEditorScreen

---

## 導航

- **進入:**
    - **來源:** SettingsScreen
- **退出:**
    - **觸發:** 頂部導航列返回按鈕
    - **導航:** SettingsScreen
- **導出:**
    - **觸發:** 點擊列表項目或新增按鈕
    - **導航:** AccountEditorScreen 或 PaywallScreen 或 MergeEditorScreen