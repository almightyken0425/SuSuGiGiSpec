# 記帳 App 規格指令

- 本 repo 是 Module Spec git。
- module id 是 `no2_accounting_app`。
- 本 repo 承載行為規格。

## 規格政策

- 修改前使用 `decision_framework_router`。
- 規格修改必須使用 `spec_writer`。
- Markdown 必須使用 `universal_writing_linter`。
- Model 位於 `no1_data_models`。
- View 位於 `no2_screens`。
- Logic 位於 `no3_logics`。
- 跨層限制套用 boundary 政策。
- 不把 Design 細節寫入 Spec。
- 不把 Impl 細節寫入 Spec。

## 命名規則

- GitHub remote slug 使用 `susugigi-spec-no2-accounting-app`。
- 獨立 clone 的預設資料夾使用 `susugigi-spec-no2-accounting-app`。
- 產品 manifest 內的實體路徑使用 module id `no2_accounting_app`。
- 自建資料夾與檔名使用 `snake_case`。
- 規格前後關係使用不補零的 `noN_` 前綴。
- repo 內的模板與指南來源檔名不得使用 shell 特殊字元。
- runtime contract 中已定義的輸出名稱沿用既有契約，不受來源檔名禁令限制。

## 多層配對

- Design 仲裁視覺與互動。
- Spec 仲裁資料與邏輯。
- Impl 跟隨兩側決議。
- Product Map 是上游整合依據。
- 配對規則以產品註冊表為準。
- 跨層分支必須逐字一致。
- 配對 commit 使用相同內容。

## 對側導覽

- Model 對應資料模型與 migration。
- View 對應 Design screens。
- View 也對應 Impl screens。
- Logic 對應 contexts 與 services。
- Logic 也對應 hooks。
- 視覺 token 具體值屬 Design。
- 元件實作規則屬 Impl。

## 共用 UI 政策

- 共用政策位於 `no2_screens/shared_ui_policies`。
- screen 只引用模式名稱。
- screen 不重述共用細節。
- Header 政策涵蓋各導航模式。
- List 政策涵蓋各列表模式。
- Search 採 Bottom Pill 模式。
- 日期選擇分兩種模式。
- editor 共用刪除行為。
- Undo 狀態由 Logic 承載。

## 產品術語

- 付費等級只用以下形式。
  - `LEVEL_0`
  - `LEVEL_1`
  - `LEVEL_2`
  - `LEVEL_3`
  - `LEVEL_B`
- 商業定義由提案層仲裁。
- 能力清單由 payment map 承載。

## 指令檔維護

- `AGENTS.md` 是規則單一真相。
- `CLAUDE.md` 僅保留相容入口。
- 不在相容入口複製規則。
