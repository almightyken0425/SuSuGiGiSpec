# 匯率規格重構紀錄 Currency Spec Refactor Log
**日期:** 2026-01-02
**範圍:** 匯率設定、顯示、預設值邏輯、帳戶與偏好設定連動

---

## 摘要 Summary
本次重構旨在將「匯率列表」轉型為「匯率儀表板」，強調以「基礎貨幣 (Base Currency)」為核心的資產估值觀點。確立了「不自動換算 (No Auto-Triangulation)」原則，並引入「主動建立預設值 (Proactive Default)」機制，確保系統中始終存在明確的匯率紀錄。

---

## 修改項目 Changes

### 1. 顯示與列表邏輯 (Display & List)
- **文件:** `no13_currency_rate_list_screen.md`
- **變更:**
    - **儀表板化:** 列表不再只是歷史紀錄，而是根據「帳戶幣別」自動列出所有需要的交易對 (Foreign / Base)。
    - **顯示標準:** 統一格式 `1 Foreign / Base` (例如 `1 USD / TWD = 32.5`)。
    - **小數位數:** 統一顯示至小數點後 6 位。
    - **搜尋:** 增加模糊搜尋功能。

### 2. 編輯器行為 (Editor Behavior)
- **文件:** `no14_currency_rate_editor_screen.md`
- **變更:**
    - **移除日期選擇:** 強制使用當下時間 (Now) 作為 `rateDate`，確保手動設定永遠生效 (Append-Only)。
    - **單一模式:** 移除「自由模式」，僅支援從列表進入的「鎖定模式」 (指定 CurrencyFrom/To)。
    - **預設填入:** 若無歷史匯率，預設填入 `1`。

### 3. "預設值為 1" 與 "主動建立" (Default Rate Logic)
- **核心原則:** 系統嚴禁使用交叉匯率自動推算。若無直接匯率紀錄，一律視為 `1:1`。
- **文件:** `no11_account_editor_screen.md`
    - **新增帳戶時:** 若該外幣尚無對應本幣的匯率，系統 **主動寫入** 一筆 `Rate=1` 的紀錄。
- **文件:** `no15_preference_screen.md`
    - **切換本幣時:** 掃描所有外幣帳戶，若對新本幣尚無匯率，系統 **主動寫入** 一筆 `Rate=1` 的紀錄。

### 4. 格式標準化 (Formatting)
- **全域:** 移除所有文件中的全形引號 `「」` 與括號 `()`，符合專案寫作規範。

---

## 影響範圍 Impact Analysis
- **Account Creation:** 新增外幣帳戶將觸發寫入 `CurrencyRates`。
- **Settings Change:** 切換 Base Currency 將觸發批量寫入 `CurrencyRates`。
- **Currency List:** 顯示內容改為動態生成，非單純讀取 DB。
- **Calculation:** 所有估值運算嚴格依賴 DB 內的實體匯率紀錄 (或 1)，不進行動態交叉計算。
