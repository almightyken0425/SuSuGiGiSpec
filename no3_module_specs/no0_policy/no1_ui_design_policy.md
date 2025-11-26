# UI 設計規範

## 核心原則

- **一致性:**
    - **行為:** App 內所有畫面的視覺風格、元件、間距必須保持高度一致
    - **工具:** 遵循 `theme.ts` 中定義的常數
- **簡潔性:**
    - **行為:** 優先採用簡潔、直覺的佈局
    - **備註:** 避免不必要的裝飾或複雜動畫
- **本地優先:**
    - **行為:** UI 必須即時反應 本機資料庫 的狀態
    - **禁止:** 顯示等待雲端同步的載入狀態
    - **備註:** 僅在手動觸發同步時顯示載入指示器

---

## 顏色

- **來源:** `src/constants/theme.ts`
- **結構:**
    - `THEME_COLORS.primary`
    - `THEME_COLORS.secondary`
    - `THEME_COLORS.background`
    - `THEME_COLORS.textPrimary`
    - `THEME_COLORS.textSecondary`
    - `THEME_COLORS.accentRed`
    - `THEME_COLORS.accentGreen`
- **禁止:** 在 `StyleSheet` 中寫死色碼

---

## 字體排版

- **來源:** `src/constants/theme.ts`
- **結構:**
    - `TYPOGRAPHY.h1`
    - `TYPOGRAPHY.h2`
    - `TYPOGRAPHY.body`
    - `TYPOGRAPHY.caption`
- **禁止:** 在 `StyleSheet` 中寫死 `fontSize` 或 `fontWeight`

---

## 間距與佈局

- **來源:** `src/constants/theme.ts`
- **結構:**
    - `SPACING.xs`
    - `SPACING.sm`
    - `SPACING.md`
    - `SPACING.lg`
- **行為:**
    - 所有元件的 `margin` `padding` 必須使用 `SPACING` 常數

---

## 元件

- **通用元件:**
    - **位置:** `src/components/common/`
    - **行為:** 建立可重用的基礎元件
    - **範例:** `Button`, `Modal`, `Card`, `Input`
- **樣式:**
    - **工具:** `StyleSheet.create`
    - **禁止:** 行內樣式

---

## 圖標 Icons

- **來源:** `IconDefinition.json`
- **工具:** `Feather Icons`
- **行為:**
    - **輔助:** 使用 `iconHelper.ts` 處理圖標名稱映射
    - **禁止:** 使用 `IconDefinition.json` 以外的圖標集

---

## 全域設計原則

- **編輯器呈現方式:**
    - **目標:** 所有 新增 或 編輯 畫面
    - **UI:** 統一採用 Sheet 形式的 Modal 呈現
    - **禁止:** 全螢幕或 Segue Push 導航