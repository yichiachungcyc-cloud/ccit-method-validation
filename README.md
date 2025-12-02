# ccit-method-validation
CCIT data cleaning, anomaly removal, 3σ filtering, reject limit calculation, and control chart automation using Python, pandas, numpy, matplotlib and SQLite.
# CCIT Method Validation & Control Chart Automation

This project performs **data cleaning**, **3σ anomaly removal**, **reject limit calculation**,  
and **automated CCIT control chart generation** using Python, pandas, numpy, matplotlib, and SQLite.

---

## 📦 Features (功能)

### ✔ 1. Data Cleaning & Preprocessing
- 移除重複與缺失值
- 統一欄位名稱
- 自動識別 System Check / Positive SPL / Negative SPL

### ✔ 2. Negative SPL 3σ Anomaly Removal
- Negative SPL 使用 3 標準差濾除異常點  
- 清洗後數據作為方法參數計算依據

### ✔ 3. CCIT Method Limit Calculation
自動計算：
- Cycle 1 Test Vac 範圍  
- Cycle 1 Diff Vac 範圍  
- Cycle 2 Test Vac 固定參數  
- Cycle 2 Diff Vac：3σ 以及 Reject Limit  
Reject Limit 依照 **0, 5, 10 rounding rule** 自動調整。

### ✔ 4. CCIT Control Chart
- 自動繪製 Negative SPL、Positive SPL、System Check 的散點管制圖
- 載入 +3σ、平均線、Reject Limit
- 對同一 Test_ID 自動加入 jitter（避免重疊）

### ✔ 5. Export to SQLite
- 自動匯出清理後資料至 `ccit_data.db`
- 可搭配 SQLife3 / DBeaver / DB Browser SQLite 檢視

---

## 📂 File Structure (專案結構)
ccit-method-validation/
│
├── ccit_analysis.py # 主程式
├── data/
│ └── ccit_raw_data-1.csv
├── ccit_data.db # 自動生成的 SQLite 資料庫
└── README.md
