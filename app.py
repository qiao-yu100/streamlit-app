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

# 計算 Weekly NCD% prediction 的原始數值（未加上 %）
summary_df['Weekly NCD% prediction_raw'] = (
    summary_df['DPW'] * summary_df['Scrap wafer'] / total_shipped_die_sum
) * 100

# 四捨五入並加上 % 字串
summary_df['Weekly NCD% prediction'] = summary_df['Weekly NCD% prediction_raw'].round(2).astype(str) + '%'

# 計算總和
weekly_ncd_sum = summary_df['Weekly NCD% prediction_raw'].sum().round(2)

'Weekly NCD% prediction': f"{weekly_ncd_sum}%"  # 加上百分比字串


# 建立 sum row
sum_row = {
    'DID': 'sum',
    'DPW': summary_df['DPW'].sum(),
    'GOOD_DIE': summary_df['GOOD_DIE'].sum(),
    'CQDR_DIE': summary_df['CQDR_DIE'].sum(),
    'Total_shipped_die': summary_df['Total_shipped_die'].sum(),
    'SQDR_DIE': summary_df['SQDR_DIE'].sum(),
     'SQDR NCD Percent': f"{(summary_df['SQDR_DIE'].sum() / summary_df['Total_shipped_die'].sum()) * 100:.2f}%",
    'GOOD_WAFER': summary_df['GOOD_WAFER'].sum(),
    'CQDR_WAFER': summary_df['CQDR_WAFER'].sum(),
    'Scrap wafer': summary_df['Scrap wafer'].sum(),
    'Weekly NCD prediction': f"{weekly_ncd_sum}%"  # 加上百分比字串
}

# 加入 sum row 到 DataFrame
summary_df = pd.concat([summary_df, pd.DataFrame([sum_row])], ignore_index=True)


# 顯示更新後的資料表
st.subheader("更新後的資料表")
st.dataframe(summary_df)








