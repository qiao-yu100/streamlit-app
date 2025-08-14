import streamlit as st
import pandas as pd

# 讀取 CSV 檔案
try:
    summary_df = pd.read_csv("summary_wip_prediction.csv")
except Exception:
    st.error("找不到 summary_wip_prediction.csv，請確認檔案是否存在於目錄中。")
    st.stop()

# 頁面標題
st.title("Baseline SQDR NCD% Summary (Rolling 5W)")

# Scrap wafer 輸入欄位
st.subheader("Scrap plan")
scrap_values = []

num_cols = 4
rows = (len(summary_df) + num_cols - 1) // num_cols

for row in range(rows):
    cols = st.columns(num_cols)
    for col in range(num_cols):
        i = row * num_cols + col
        if i < len(summary_df):
            with cols[col]:
                scrap = st.number_input(
                    label=f"{summary_df.at[i, 'DID']} Scrap wafer",
                    min_value=0.0,
                    value=0.0,
                    step=1.0,
                    key=f"scrap_{i}"
                )
                scrap_values.append(scrap)

# 加入 Scrap wafer 欄位
summary_df['Scrap wafer'] = scrap_values

# 計算 Weekly NCD prediction
total_shipped_die_sum = summary_df['Total_shipped_die'].sum()
summary_df['Weekly NCD prediction_raw'] = (
    summary_df['DPW'] * summary_df['Scrap wafer'] / total_shipped_die_sum
) * 100
summary_df['Weekly NCD prediction'] = summary_df['Weekly NCD prediction_raw'].round(2).astype(str) + '%'
weekly_ncd_sum = summary_df['Weekly NCD prediction_raw'].sum().round(2)

# 建立 sum row
sum_row = {
    'DID': 'sum',
    'WIP Projection': summary_df['WIP Projection'].sum(),
    'GOOD_DIE': summary_df['GOOD_DIE'].sum(),
    'CQDR_DIE': summary_df['CQDR_DIE'].sum(),
    'EVENT_QDR_DIE': summary_df['EVENT_QDR_DIE'].sum(),
    'Total_shipped_die': summary_df['Total_shipped_die'].sum(),
    'SQDR_DIE': summary_df['PLANNED_QDR_DIE'].sum(),
    'PLANNED_QDR_DIE': summary_df['SQDR_DIE'].sum(),
    'SQDR NCD Percent': f"{(summary_df['SQDR_DIE'].sum() / summary_df['Total_shipped_die'].sum()) * 100:.2f}%",
    'GOOD_WAFER': summary_df['GOOD_WAFER'].sum(),
    'CQDR_WAFER': summary_df['CQDR_WAFER'].sum(),
    'SQDR_WAFER': summary_df['SQDR_WAFER'].sum(),
    'EVENT_QDR_WAFER': summary_df['EVENT_QDR_WAFER'].sum(),
    'PLANNED_QDR_WAFER': summary_df['PLANNED_QDR_WAFER'].sum(),
    'Scrap wafer': summary_df['Scrap wafer'].sum(),
    'Weekly NCD prediction': f"{weekly_ncd_sum}%"
}
summary_df = pd.concat([summary_df, pd.DataFrame([sum_row])], ignore_index=True)

# 顯示資料表
st.subheader("Baseline SQDR NCD% Summary (4RA)")
display_df = summary_df.drop(columns=['Weekly NCD prediction_raw'])

# 建立 HTML 表格並加上背景色
def df_to_colored_html(df, highlight_cols):
    html = '<table style="border-collapse: collapse; width: 100%;">'
    html += '<thead><tr>'
    for col in df.columns:
        html += f'<th style="border:1px solid black;padding:4px;">{col}</th>'
    html += '</tr></thead><tbody>'
    for _, row in df.iterrows():
        html += '<tr>'
        for col in df.columns:
            style = 'background-color: #D6EAF8;' if col in highlight_cols else ''
            html += f'<td style="border:1px solid black;padding:4px;{style}">{row[col]}</td>'
        html += '</tr>'
    html += '</tbody></table>'
    return html

# 指定要加背景色的欄位
highlight_columns = ['WIP Projection', 'Scrap wafer', 'Weekly NCD prediction']
html_table = df_to_colored_html(display_df, highlight_columns)

# 顯示 HTML 表格
st.markdown(html_table, unsafe_allow_html=True)





















