# 偏好上傳邏輯: PreferenceUploadLogic

## 目的

- CloudSync 與 PreferenceUpload 軌的唯一承載點
- 同時涵蓋上傳政策與 Firestore 偏好寫入端
- 只上傳、不下載
- 本機 Settings 表為偏好唯一真相
- 雲端偏好永不回套至本機
- 無衝突解決機制
- 多裝置各自上傳，接受最後寫入覆寫
- 上傳目的為未來資料分析維度，分析管線當前未接
- BigQuery mirror 不納入 preference，上傳資料留存 Firestore、暫無分析管線消費
- 全 user 享有，不做 Premium 篩選
- 不使用 Real-time listener

---

## getUploadedPreferenceFields 取得上傳欄位清單

- 回傳所有參與上傳的 preference 欄位識別碼

- **回傳:**
  - 欄位識別碼清單
    - baseCurrencyId
    - theme
    - language
    - timeZone
    - launchMode
    - weekStart
    - analyticsConsent

---

## uploadPreferences 上傳偏好設定

- CloudSync 與 PreferenceUpload 軌的 Firestore 寫入端

- **輸入:**
  - 欲變更的偏好欄位與目標值，未傳入的欄位不受影響
- **執行:**
  - **IF** 無登入使用者:
    - 跳過雲端寫入
  - **ELSE:**
    - 逐欄將本機偏好欄位映射為遠端欄位後，以 dot notation 更新 preferences，避免覆寫整個 preferences 物件
    - 欄位映射與值轉換規則:
      - `baseCurrencyId` 上傳為遠端 `currency`，值由數值幣別 ID 轉為 ISO 4217 代碼字串，無法解析則略過該欄位
      - `timeZone` 上傳為遠端 `timezone`，值直送
      - `launchMode` 值正規化，非 `home` / `expense` / `income` / `transfer` 一律改為 `home`
      - `weekStart` 值正規化，非 `auto` / `sunday` / `monday` 一律改為 `auto`
      - `analyticsConsent` 遷移自舊資料的 Null 視為 `true`，代表已同意
      - `theme`、`language` 欄位名與值皆直送
      - 任一欄位轉換後值為空值或 Null 者，略過不寫入
    - 自動更新文件根層 updatedAt 為當下時間，無論傳入欄位數量
    - updatedAt 僅標記文件最後寫入時間，無消費端，不參與衝突解決
    - **IF** Firestore 寫入失敗:
      - 僅記 log，不阻塞 UI

---

## uploadAllPreferences 全量上傳本機偏好

- 將本機 Settings 全部偏好欄位一次上傳雲端
- 供 PostAuthLogic 的 handlePostAuth 呼叫

- **執行:**
  - 讀取本機 Settings 表中各偏好欄位的實際值
  - 涵蓋 getUploadedPreferenceFields 列舉的全部欄位
  - 委派 uploadPreferences，帶入全欄位與本機實際值
