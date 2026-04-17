# 主題設定: ThemeSettingsScreen

## 畫面目標

- 提供瀏覽、切換並即時預覽 App 配色主題的介面

---

## 線框圖

```text
+--------------------------------+
| < Back      Themes             |
+--------------------------------+
| [ Preview ]   [ Preview ]      |
| Name (Light)  Name (Dark)      |
| [ Selected ]                   |
|                                |
| [ Preview ]   [ Preview ]      |
| Name (Light)  Name (Dark)      |
+--------------------------------+
```

---

## 佈局

### 導覽列

- 返回按鈕
- 配色主題 標題

### 主題列表

- 主題卡片
  - 配色預覽區
  - 主題名稱
  - Light 或 Dark 標籤
  - **IF** 當前已選主題:
    - 顯示選取標記

---

## 互動

- **點按返回按鈕:**
  - 返回上一頁

- **點按主題卡片:**
  - 呼叫 applyTheme
  - App 即時套用新主題配色
