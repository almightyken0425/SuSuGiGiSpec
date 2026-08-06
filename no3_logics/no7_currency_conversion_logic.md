# 匯率轉換邏輯: CurrencyConversionLogic

## 目的

- 定義多幣別金額換算規則，確保各介面的金額顯示一致

---

## resolveCurrencyRate 查找匯率

- 給定幣別對，查找最新已生效匯率，回傳主單位對主單位匯率
- 僅查原始幣別與主要貨幣的直接記錄，不經中間幣別接力換算；無已生效記錄時回 1
- **輸入:**
  - 原始幣別
  - 主要貨幣
- **性質:**
  - 純本地計算，不發出網路請求
- **執行:**
  - 合併原始幣別與主要貨幣之間的正向與反向所有交易對
  - 排除生效時點晚於當下的記錄；未來時點的記錄尚未生效，例如未來日期跨幣別轉帳的連動補錄，待該時點到達才參與選取
  - 依生效時點倒序排列；生效時點相同時，再依記錄更新時間倒序，取最新一筆
  - 同一生效時點可能有多筆，例如同一筆轉帳未改日期而多次編輯金額時，補錄記錄皆沿用該轉帳發生時點，以更新時間最新者為準，確保最後一次編輯生效
  - **IF** 無任何已生效記錄:
    - **回傳:** 匯率 1
  - **ELSE:**
    - **IF** 最新記錄為正向:
      - **回傳:** 該記錄的匯率
    - **ELSE:**
      - **回傳:** 該記錄匯率的倒數

---

## getCurrencyPairs 列出帳戶幣別對

- 為匯率列表畫面組裝顯示用的幣別對清單
- **輸入:**
  - 主要貨幣
- **性質:**
  - 純本地計算，不發出網路請求
- **執行:**
  - 蒐集所有帳戶使用、且不等於主要貨幣的外幣，去除重複
  - 對每個外幣與主要貨幣配對，以 resolveCurrencyRate 查找該對匯率
- **回傳:**
  - 各外幣對主要貨幣的幣別對與匯率清單

---

## createInitialCurrencyRate 建立初始匯率

- 為新建立的非主要貨幣帳戶種入一筆佔位匯率，供後續換算使用
- 種入的匯率值固定為 1，僅作佔位
- 佔位記錄的 `date` 固定為極早的佔位時點，不取建立當下時刻
- 任何真實匯率記錄的 `date` 皆晚於佔位時點，經 resolveCurrencyRate 選取必然壓過佔位；真實記錄較佔位晚寫入、`date` 較舊時亦同
- 該幣別對僅有佔位記錄時，佔位照樣被選取，換算結果為 1
- 真實匯率待後續 createTransfer 連動產生，或由使用者透過 createCurrencyRate 手動修正
- 匯入不呼叫本操作；匯入僅透過 createTransaction 與 createTransfer 建立資料，跨幣別匯率由 createTransfer 連動產生，無記錄則 resolveCurrencyRate 回傳 1
- **輸入:**
  - 原始幣別
  - 主要貨幣
- **寫入 CurrencyRate:**
  - **執行:**
    - **IF** 該幣別對尚無記錄:
      - 新增一筆匯率值為 1 的記錄至 `CurrencyRates` 表
    - **ELSE:**
      - 不重複種入
  - **欄位:**
    - date: 極早的佔位時點，不取建立當下時刻

---

## createCurrencyRate 手動新增匯率

- 使用者在匯率編輯器對既有幣別對手動輸入匯率，寫入一筆匯率記錄；與 createInitialCurrencyRate 的帳戶初始化入口區隔
- **輸入:**
  - 來源幣別
  - 目標幣別
  - 匯率
  - 生效時點，手動記錄當下的日期與時刻
- **匯率守門:**
  - 匯率須為有限正值：不得為零、負數、非數值或無限大。
  - 不設單一寫死的匯率天花板。匯率量級的合理上界由來源金額輸入的位數上限與匯率編輯兩金額欄的即時過濾共同界定——兩欄各只接受有限位數的數字與單一小數點，其比值自然框住匯率量級。刻意不寫死單一匯率上限，以免對惡性通膨幣別的高量級匯率不友善。
- **寫入 CurrencyRate:**
  - **執行:**
    - **IF** 匯率非有限正值:
      - **回傳:** 驗證失敗，失敗原因為匯率非有限正值
    - **ELSE:**
      - 新增一筆記錄至 `CurrencyRates` 表

---

## resolveTransferDisplay 取得轉帳顯示資料

- 依所選帳戶範圍，判斷轉帳的顯示方式及是否需要換算
- **輸入:**
  - 轉帳紀錄
  - 已選帳戶清單
- **性質:**
  - 純本地計算，不發出網路請求
- **執行:**
  - **IF** 轉出帳戶與轉入帳戶皆在已選清單內:
    - **回傳:** 不顯示，屬內部轉帳
  - **IF** 轉出帳戶與轉入帳戶皆不在已選清單內:
    - **回傳:** 不顯示，與所選帳戶無關
  - **IF** 轉出帳戶在已選清單內:
    - **IF** amountFrom 的幣別不等於主要貨幣:
      - **回傳:** 查找適用匯率後換算為主要貨幣的支出金額
    - **ELSE:**
      - **回傳:** 以 amountFrom 顯示為支出
  - **ELSE:**
    - **IF** amountTo 的幣別不等於主要貨幣:
      - **回傳:** 查找適用匯率後換算為主要貨幣的收入金額
    - **ELSE:**
      - **回傳:** 以 amountTo 顯示為收入

---

## getMinorUnits 取貨幣 minorUnits

- 給定貨幣，回傳該貨幣定義的 minorUnits 小數位數
- 純顯示用途，不影響儲存縮放
- 未知貨幣 fallback 為 2，不對任何貨幣設特例
- **輸入:**
  - 目標貨幣
- **性質:**
  - 純本地計算，不發出網路請求
- **執行:**
  - **IF** 該貨幣在 Currencies 中有定義:
    - **回傳:** 該貨幣定義的 `minorUnits`
  - **ELSE:**
    - **回傳:** 預設位數 2

---

## getCurrencyConfig 解析貨幣顯示設定

- 給定貨幣，回傳顯示用的 decimals 與 useThousandsUnit 兩項設定
- decimals 優先序：使用者 CurrencyConfig 的 `decimalPlaces` > TWD UX 例外 0 > 該貨幣 minorUnits
- TWD 例外 0 是本操作內為台灣使用者偏好設的顯示預設，非 getMinorUnits 推導；TWD 的 minorUnits 實為 2，此例外會被使用者設定的 `decimalPlaces` 覆寫
- **輸入:**
  - 目標貨幣
- **性質:**
  - 純本地計算，不發出網路請求
- **執行:**
  - **IF** 該貨幣無對應 id:
    - **回傳:** decimals 2 與 useThousandsUnit 關閉
  - **ELSE:**
    - 取該貨幣的 minorUnits 作為 decimals 起始值
    - **IF** 該貨幣的 CurrencyConfig 存在且 `decimalPlaces` 非 Null:
      - decimals 改取 `decimalPlaces`
    - **IF** 目標貨幣為 TWD 且 `decimalPlaces` 為 Null:
      - decimals 改為 0
    - useThousandsUnit 取該貨幣 CurrencyConfig 的 `useThousandsUnit`，無 CurrencyConfig 時為關閉
    - **回傳:** decimals 與 useThousandsUnit

---

## formatCurrency 依幣別格式化金額

- 將整數縮放儲存值還原為依該幣別顯示設定格式化的顯示字串，作為各介面金額顯示的單一來源
- decimals 與 useThousandsUnit 不由呼叫端傳入，內部以 currencyCode 經 getCurrencyConfig 取得
- **輸入:**
  - 整數縮放金額
  - 目標幣別
- **性質:**
  - 純本地計算，不發出網路請求
- **執行:**
  - 以目標幣別經 getCurrencyConfig 取得 decimals 與 useThousandsUnit
  - **IF** useThousandsUnit 啟用:
    - 整數縮放金額先除以一千，進入以千為單位的 K 顯示模式
  - 結果再除以一萬還原為主單位數值，與存檔端乘以一萬的固定倍率縮放對齊
  - 依 decimals 格式化為顯示字串
- **回傳:**
  - 格式化後的金額顯示字串
