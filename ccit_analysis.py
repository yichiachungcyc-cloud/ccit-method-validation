import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3

# -----------------------------
# 1️⃣ 匯入資料
# -----------------------------
df = pd.read_csv("ccit_raw_data-1.csv", encoding="utf-8-sig")

# -----------------------------
# 2️⃣ 清理資料
# -----------------------------
df = df.drop_duplicates()
df = df.dropna(subset=['Test ID. (Samples)', 'Cycle 2_Pa'])

# -----------------------------
# 3️⃣ 統一欄位名稱
# -----------------------------
df.rename(columns={
    'Test No.': 'Test_No',
    'Test ID. (Samples)': 'Test_ID',
    'Cycle 1_mbar': 'Cycle1_mbar',
    'Cycle 1_Pa': 'Cycle1_Pa',
    'Cycle 2_mbr': 'Cycle2_mbar',
    'Cycle 2_Pa': 'Cycle2_Pa',
    'Comments': 'Comments'
}, inplace=True)

# -----------------------------
# 4️⃣ 型態轉換
# -----------------------------
df['Test_ID'] = df['Test_ID'].astype(float, errors='ignore')
df['Cycle2_Pa'] = pd.to_numeric(df['Cycle2_Pa'], errors='coerce')

# -----------------------------
# 5️⃣ 樣本分類
# -----------------------------
def classify_sample(x):
    if x in [0.1, 0.5]:
        return "System check"
    elif x == 41:
        return "Positive SPL"
    else:
        return "Negative SPL"

df['Type'] = df['Test_ID'].apply(classify_sample)

# -----------------------------
# 6️⃣ 移除 Negative SPL >3σ 異常值
# -----------------------------
neg = df[df['Type'] == 'Negative SPL'].copy()
neg_mean_orig = neg['Cycle2_Pa'].mean()
neg_std_orig = neg['Cycle2_Pa'].std()
neg_clean = neg[abs(neg['Cycle2_Pa'] - neg_mean_orig) <= 3*neg_std_orig].copy()

# 用清理後的 Negative SPL 替換原本的資料
df_clean = pd.concat([df[df['Type'] != 'Negative SPL'], neg_clean])

# -----------------------------
# 7️⃣ 計算方法參數上下限
# -----------------------------
# Cycle1_mbar
cycle1_mbar_mean = neg_clean['Cycle1_mbar'].mean()
cycle1_mbar_lower = cycle1_mbar_mean - 50
cycle1_mbar_upper = cycle1_mbar_mean + 50

# Cycle1_Pa & Cycle2_mbar 固定值
cycle1_pa_lower, cycle1_pa_upper = -5, 50
cycle2_mbar_lower, cycle2_mbar_upper = 0, 10

# Cycle2_Pa & Reject Limit
neg_mean = neg_clean['Cycle2_Pa'].mean()
neg_std = neg_clean['Cycle2_Pa'].std()
pos_mean = df[df['Type'] == 'Positive SPL']['Cycle2_Pa'].mean()

cycle2_pa_lower = neg_mean - 3*neg_std
cycle2_pa_upper = neg_mean + 3*neg_std

# Reject Limit 尾數規則
def adjust_to_0_5_10(x):
    x_rounded = int(round(x))
    r = x_rounded % 10
    if r in [0,1,2,3]:
        return x_rounded - r
    elif r == 4:
        return x_rounded - r + 5
    elif r in [5,6,7,8]:
        return x_rounded - r + 5
    else:  # r == 9
        return x_rounded - r + 10

reject_limit_upper = adjust_to_0_5_10((pos_mean + cycle2_pa_upper)/2)
reject_limit_lower = -5

# -----------------------------
# 8️⃣ 整理方法參數表格
# -----------------------------
limits = pd.DataFrame({
    "Parameter": ["Cycle1_mbar", "Cycle1_Pa", "Cycle2_mbar", "Cycle2_Pa", "Reject Limit"],
    "Lower Limit": [cycle1_mbar_lower, cycle1_pa_lower, cycle2_mbar_lower, cycle2_pa_lower, reject_limit_lower],
    "Upper Limit": [cycle1_mbar_upper, cycle1_pa_upper, cycle2_mbar_upper, cycle2_pa_upper, reject_limit_upper]
})

# 顯示表格（有框線）
from tabulate import tabulate
print("✅ Result：")
print(tabulate(limits, headers='keys', tablefmt='fancy_grid', showindex=False))



# -----------------------------
# 9️⃣ 繪製管制圖
# -----------------------------
plt.figure(figsize=(14,6))

# 為同一 Test_ID 點加 jitter
df_clean['x_jitter'] = df_clean['Test_ID'] + (np.random.rand(len(df_clean)) - 0.5) * 0.1

for t, color in [('Negative SPL', 'blue'), ('System check', 'gray'), ('Positive SPL', 'red')]:
    subset = df_clean[df_clean['Type'] == t]
    plt.scatter(subset['x_jitter'], subset['Cycle2_Pa'], color=color, alpha=0.7, label=t)

plt.axhline(neg_mean, color='green', linestyle='--', label='Neg SPL Avg')
plt.axhline(cycle2_pa_upper, color='red', linestyle='--', label='+3σ')
plt.axhline(neg_mean - 3*neg_std, color='red', linestyle='--', label='-3σ')
plt.axhline(reject_limit_upper, color='purple', linestyle=':', label='Reject Limit')

plt.title("CCIT Control Chart (Cycle2_Pa, Cleaned Data)")
plt.xlabel("Test_ID")
plt.ylabel("Cycle2_Pa")
plt.xticks(sorted(df_clean['Test_ID'].unique()))
plt.legend()
plt.grid(True)
plt.show()

# -----------------------------
# 8️⃣ 整理方法參數表格
# -----------------------------
limits = pd.DataFrame({
    "Parameter": ["Cycle 1 Test Vac", "Cycle 1 Diff Vac", "Cycle 2 Test Vac", "Cycle 2 Diff Vac"],
    "Min": [cycle1_mbar_lower, cycle1_pa_lower, cycle2_mbar_lower, reject_limit_lower],
    "Max": [cycle1_mbar_upper, cycle1_pa_upper, cycle2_mbar_upper, reject_limit_upper]
})

# 顯示表格（有框線）
from tabulate import tabulate
print("✅ Reject References：")
print(tabulate(limits, headers='keys', tablefmt='fancy_grid', showindex=False))

# -----------------------------
# 🔟 匯出至 SQLite (SQLife3)
# -----------------------------
conn = sqlite3.connect("ccit_data.db")
df_clean.to_sql("ccit_table", conn, if_exists="replace", index=False)
conn.close()
print("✅ 已成功建立 ccit_data.db，可在 SQLife3 開啟！")
