# 產品組件與價值分配

## 核心目標

- 本文件依據產品定義的產品個體，詳細列出每個組件的價值構成。
- 採用 **雙重價值模型**：每個模組同時包含 **施工價值** Construction 與 **維運價值** Operation。
- 針對每個 **User Story**，依據角色定義進行價值點數分配。
- **營運角色整合:** Marketing 與 Operations 角色整合至每個 User Story 中，其施工價值為 0，但隨著功能上線，其維運價值 Operation Value 將逐步累積。
- **價值單位:** 1 點 = 0.1 小時，詳見股權原則文件。

---

## 1. 記帳 App + Firestore, Accounting App

## 詳細價值分配數據

> **⚠️ 注意：** 為了確保單一事實來源 (Single Source of Truth)，所有詳細的產品組件價值分配數據（包含施工價值與維運價值）已移至 [`product_value_allocation.csv`](product_value_allocation.csv) 統一維護。
>
> 請直接參考該 CSV 檔案以獲取最新、最準確的數據。本文件僅保留架構性說明（如有）。

[點擊開啟 product_value_allocation.csv](product_value_allocation.csv)
