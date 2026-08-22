# 身分後初始化流程: PostAuthLogic

## handlePostAuth 處理身分後初始化

- 身分就緒後依本機與雲端資料是否存在分派初始化路徑
- 身分來源為匿名建立、熱啟動沿用、或 legacy 登入帳號升級沿用，路徑一致
- 全 user 一致、無條件執行，不分訂閱等級
- Premium 狀態刷新由 PremiumLogic 的 refreshStatus 承載，不在本流程內，bootstrap 不等待 IAP 服務回應
- 資料清除中斷復原命中時整段跳過，不得重建剛刪除的雲端文件，詳見 DeleteUserAccountLogic
- **執行:**
  - 讀取 Firestore `users/{uid}` 文件的存在性
  - **IF** 本機無此帳號的 Users 與 Settings 紀錄:
    - 呼叫 initializeLocalUser
  - 呼叫 initializeDefaultEntities
  - **IF** 文件不存在:
    - 呼叫 initializeCloudUser
  - **ELSE:**
    - 委派 PreferenceUploadLogic 的 uploadAllPreferences，上傳本機實際值並接受覆寫雲端
  - 不再讀取並套用雲端 preference，不依文件存在與否決定是否下載

---

## initializeLocalUser 初始化本機使用者資料

- 依裝置 Locale 推導預設值，建立本機 Users 與 Settings 紀錄
- **性質:**
  - 純本機，無雲端動作
- **決定預設值:**
  - **執行:**
    - 主要貨幣:
      - 從裝置 Locale 推導
      - 若無則預設 TWD，並轉換為 Currency ID
    - 語系:
      - 從裝置 Locale 推導，與支援語系清單比對
      - 比對成功則採該語系
      - 比對未匹配則 fallback 預設 en
      - 不做語族內 fallback，避免繁簡混雜或非預期語系出現
    - 時區:
      - 讀取裝置時區
    - 主題:
      - 預設 theme1
    - 啟動模式:
      - 預設 home
    - 週起始日:
      - 預設 auto，代表依使用者語系慣例決定，不做 Locale 推導
- **建立本機資料:**
  - **執行:**
    - 新增記錄至 Users 表與 Settings 表
  - **欄位:**
    - `baseCurrencyId`: 依主要貨幣決定
    - `language`: 依語系決定
    - `timeZone`: 依時區決定
    - `theme`: theme1
    - `launchMode`: home
    - `weekStart`: auto

---

## initializeDefaultEntities 建立預設記帳資料

- 帳戶與類別皆無紀錄時建立預設資料
- **性質:**
  - 純本機，無雲端動作
- **執行:**
  - 查詢目前使用者的全部帳戶與類別
  - 查詢範圍包含已刪除紀錄
  - **IF** 任一帳戶或類別已存在:
    - **回傳:**
      - 不建立任何資料
  - **ELSE:**
    - 建立現金與信用卡帳戶
    - 兩個帳戶皆採主要貨幣
    - 建立三個支出類別
    - 建立兩個收入類別
    - 名稱採本機設定語系
    - 不建立交易、轉帳與排程

---

## initializeCloudUser 建立雲端用戶文件

- 在 Firestore 建立 `users/{uid}` 文件，preferences 取本機 Settings 實際值
- 無條件建立，不分訂閱等級
- **建立雲端用戶文件:**
  - **執行:**
    - 在 Firestore 建立 `users/{uid}` 文件
    - preferences 欄位取本機 Settings 的實際值，而非寫死預設
  - **欄位:**
    - `uid`
    - `email`: 恆為空值；不收集身分欄位，legacy 登入帳號亦不上傳
    - `provider`: 匿名身分標 anonymous；legacy 登入帳號照其登入門真值
    - `createdAt`
    - `preferences`
