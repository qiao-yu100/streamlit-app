import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 讀取資料
summary_df = pd.read_csv("summary_wip_prediction.csv")

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

summary_df['Scrap wafer'] = scrap_values
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

# 建立 Bootstrap 表格 HTML
def generate_bootstrap_table(df, highlight_cols):
    table_html = """
    https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css
    <table class="table table-bordered table-sm" style="font-size:14px;">
        <thead class="table-dark">
            <tr>
    """
    for col in df.columns:
        table_html += f"<th>{col}</th>"
    table_html += "</tr></thead><tbody>"

    for _, row in df.iterrows():
        table_html += "<tr>"
        for col in df.columns:
            style = "background-color:#D6EAF8;" if col in highlight_cols else ""
            table_html += f"<td style='{style}'>{row[col]}</td>"
        table_html += "</tr>"
    table_html += "</tbody></table>"
    return table_html

highlight_columns = ['WIP Projection', 'Scrap wafer', 'Weekly NCD prediction']
html_table = generate_bootstrap_table(display_df, highlight_columns)

# 使用 components.html 顯示表格
components.html(html_table, height=600, scrolling=True)























