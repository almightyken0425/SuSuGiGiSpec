# 設計決策權衡, Trade-offs

- **Firestore 讀寫成本 vs 使用者體驗**
    - **決策:** 選擇即時寫入以確保體驗
    - **權衡:** 接受較高的寫入次數 (Cost)，換取使用者在多裝置間無縫切換的體驗 (UX)。
    - **緩解:** 偏好設定變更頻率極低，實際成本影響有限。

- **Server-Side 訂閱管理 vs Client-Side**
    - **決策:** 選擇 Server-Side (RevenueCat)
    - **權衡:** 犧牲一點即時性 (Webhook 延遲)，換取安全性與準確性。
    - **理由:** 避免 Client 端被破解或竄改訂閱狀態，且 RevenueCat 能處理複雜的跨平台訂閱邏輯。

- **Firebase/RevenueCat vs 自建 Server**
    - **決策:** 選擇 Firebase Auth/DB 與 RevenueCat 託管
    - **權衡:** 犧牲部分資料庫結構的彈性 (NoSQL 限制) 與對底層的完全控制權。
    - **理由:** 大幅降低維運成本 (Ops Cost) 與開發複雜度，讓團隊能專注於 App 核心功能開發。
