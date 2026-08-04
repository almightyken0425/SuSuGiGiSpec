# 無帳號 bootstrap 流程: AnonymousBootstrapLogic

## 目的

- App 無登入功能、無任何帳號 UI
- 唯一身分形態為 Firebase Auth 匿名帳號，領真 uid
- 身分純內部，任何畫面不得曝露 uid
- 初次啟動自動建立匿名身分，熱啟動沿用既有身分
- 既有第三方登入帳號的裝置升級後沿用原 uid，不重建身分

---

## ensureAnonymousUser 建立匿名身分

- 身分事件回報無身分且無資料清除旗標時觸發，向 Firebase Auth 領新匿名 uid
- **性質:**
  - 非同步，需處理離線失敗
- **執行:**
  - **IF** 已有一次建立進行中:
    - 共用該次結果，不重複發起
  - 觸發 Firebase Auth 匿名登入
  - **IF** 建立失敗:
    - 標記 bootstrap 卡點為離線型態，導航層顯示 OfflineRetryScreen
    - 結束載入狀態
    - 不自動重試，重試由 retryBootstrap 驅動
  - **ELSE:**
    - 不在此接續後續流程，身分事件回報新身分後由 handleAuthEvent 收斂
- **理由:**
  - 單飛防重入：身分事件可能連續觸發；匿名登入本身冪等，極端時序不產生第二顆 uid
  - 建立中殺 App 無害：Firebase 端已建出帳號時憑證入 keychain，下次啟動即沿用；未建成則下次啟動重走一次
  - 失敗後身分事件不再回報，唯一重試驅動者是重試操作

---

## handleAuthEvent 處理身分事件

- Firebase Auth 身分事件的唯一處理入口，身分監聽與 retryBootstrap 共用
- **執行:**
  - **IF** 事件帶身分:
    - **IF** 資料清除持久旗標存在且 uid 相符:
      - 依 DeleteUserAccountLogic 的清除中斷復原判定
      - RETURN
    - **IF** 同 uid 的 post auth 流程已在跑或已跑完:
      - 等待既有流程收斂，不重跑冷啟動專屬工作
      - **IF** 既有流程失敗且標記已清:
        - 本次事件補跑一次完整流程，不迴圈
    - **ELSE:**
      - 呼叫 handlePostAuth 走完整流程
    - 清除 bootstrap 卡點標記，結束載入狀態
  - **ELSE:**
    - 清除本地身分狀態
    - **IF** 資料清除持久旗標存在:
      - 依 DeleteUserAccountLogic 的重生抑制與補收尾規則
      - RETURN
    - 呼叫 ensureAnonymousUser
- **理由:**
  - 同 uid 去重：身分監聽於前景恢復的憑證刷新也會重新觸發，冷啟動甚至連續同步觸發兩次；不去重會重跑排程補產生等冷啟動工作
  - 補跑上限一次：維持暫時性失敗的自我復原力，同時避免失敗迴圈
  - 無身分且無清除旗標涵蓋初次啟動與清除後重生兩情境，同走匿名建立

---

## retryBootstrap 重試 bootstrap

- OfflineRetryScreen 的重試操作，以當前身分狀態重驅一輪 handleAuthEvent
- **執行:**
  - 進入載入狀態
  - 讀取當前 Firebase Auth 身分，交給 handleAuthEvent
- **理由:**
  - 三種卡住情境共用一個入口：匿名建立失敗、post auth 失敗、清除復原判定不明
