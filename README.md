# CCIT Method Validation & Control Chart Automation  
**Data Analytics Project | Pharmaceutical Quality Control (GMP)**

---

## 📊 Sample Output

### 🔹 CCIT Control Chart (Cycle2_Pa)
plt.savefig("assets/control_chart.png", dpi=300, bbox_inches='tight')
👉 Automatically generated control chart with:
- Mean line  
- ±3σ limits  
- Reject limit  
- Jittered data points to avoid overlap  

---

### 🔹 Method Validation Result

![Validation Table](./assets/validation_table.png)

👉 Automatically calculated parameter limits using statistical rules and GMP-style rounding logic  

---

## 📌 Project Overview

This project demonstrates how data analytics can be applied in a **GMP-regulated pharmaceutical environment** to improve:

- Method validation  
- Anomaly detection  
- Process monitoring  

The solution automates CCIT data analysis, reducing manual workload and enabling **data-driven QC decision-making**.

---

## 🎯 Business Problem

In pharmaceutical QC environments:

- Manual CCIT analysis is time-consuming and error-prone  
- Outlier handling lacks consistency  
- No standardized reject limit calculation  
- Limited real-time monitoring  

👉 Resulting in risk to:
- Product quality decisions  
- GMP compliance  
- OOS/OOT investigation efficiency  

---

## 💡 Solution

Built an **end-to-end data analysis pipeline** using Python:

- Data cleaning & preprocessing  
- 3σ anomaly detection  
- Method validation automation  
- Control chart generation  
- SQLite database integration  

---

## 🛠️ Tech Stack

- Python (pandas, numpy)  
- matplotlib (visualization)  
- SQLite (data storage)  

---

## 🔍 Key Features

### ✔ Data Cleaning
- Removed duplicates and missing values  
- Standardized column names  

---

### ✔ 3σ Anomaly Detection
- Applied statistical filtering to Negative SPL  
- Improved consistency in outlier handling  

---

### ✔ Method Validation
- Automated parameter limit calculation  
- Implemented **0–5–10 rounding rule**  

---

### ✔ Control Chart Automation
- Generated charts for:
  - Negative SPL  
  - Positive SPL  
  - System Check  

---

### ✔ Database Export
- Stored processed data in SQLite  
- Ready for BI tools integration  

---

## 📊 Business Impact

- Reduced manual data processing time  
- Improved consistency in QC decision-making  
- Enhanced visibility of process trends  
- Strengthened GMP data integrity  

---

## 📂 Project Structure
ccit-method-validation/
│
├── ccit_analysis.py
├── data/
├── assets/ plt.savefig("assets/control_chart.png", dpi=300, bbox_inches='tight')
│ ├── control_chart.png
│ └── validation_table.png
├── ccit_data.db
└── README.md
