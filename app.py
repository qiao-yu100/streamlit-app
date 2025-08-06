import streamlit as st
import pandas as pd

# 讀取 Excel 檔案
summary_df = pd.read_csv("summary_output.csv")


# 顯示原始資料
st.title("Summary Data with Scrap Wafer Input")
st.dataframe(summary_df)

# 新增 Scrap wafer 輸入欄位
st.subheader("請輸入每一列的 Scrap wafer 數量")
scrap_values = []

for i in range(len(summary_df)):
    scrap = st.number_input(
        label=f"{summary_df.at[i, 'DID']} 的 Scrap wafer",
        min_value=0.0,
        value=0.0,
        step=1.0,
        key=f"scrap_{i}"
    )
    scrap_values.append(scrap)

# 加入 Scrap wafer 欄位
summary_df['Scrap wafer'] = scrap_values

# 計算 Weekly NCD% prediction
total_shipped_die_sum = summary_df['Total_shipped_die'].sum()/2
summary_df['Weekly NCD% prediction'] = summary_df['DPW'] * summary_df['Scrap wafer'] / total_shipped_die_sum

# 顯示更新後的資料表
st.subheader("更新後的資料表")
st.dataframe(summary_df)





