import streamlit as st
import pandas as pd

# 讀取 Excel 檔案
summary_df = pd.read_csv("summary_wip_prediction.csv")

# 設定頁面標題
st.title("Baseline SQDR Calculator")

st.subheader("Scrap plan")
scrap_values = []

# 定義分類標題
category_titles = {
    "110s": "1",
    "120s": "2",
    "130s": "3",
    "140s": "4",
    "150s": "5",
    "160s": "6",
}

# 建立分類容器
categorized_data = {title: [] for title in category_titles}

# 將 summary_df 按照 DID 第二個字母分類
for i in range(len(summary_df)):
    did = str(summary_df.at[i, 'DID'])
    if len(did) >= 2:
        second_char = did[1]
        for title, key_char in category_titles.items():
            if second_char == key_char:
                categorized_data[title].append(i)
                break

# 顯示每個分類的小標題與輸入欄位
num_cols = 4
for title, indices in categorized_data.items():
    if indices:
        st.markdown(f"### {title}")
        rows = (len(indices) + num_cols - 1) // num_cols
        for row in range(rows):
            cols = st.columns(num_cols)
            for col in range(num_cols):
                idx = row * num_cols + col
                if idx < len(indices):
                    i = indices[idx]
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


# 新增中間的 DataFrame
new_df = summary_df[['DID', 'MDPW', 'DPW', 'CPW', 'Scrap wafer']].copy()
new_df['Concentration Factor'] = 0.65

# 計算 Weekly NCD% prediction
total_shipped_die_sum = summary_df['Total_shipped_die'].sum()

# 計算 Weekly NCD prediction 的原始數值（未加上 %）
summary_df['Weekly NCD prediction_raw'] = (
    summary_df['DPW'] * summary_df['Scrap wafer'] / total_shipped_die_sum
) * 100

# 四捨五入並加上 % 字串
new_df['Weekly NCD prediction'] = summary_df['Weekly NCD prediction_raw'].round(2).astype(str) + '%'

# 計算總和
weekly_ncd_sum = summary_df['Weekly NCD prediction_raw'].sum().round(2)

# 計算 Weekly CoNC prediction
new_df['Weekly CoNC prediction'] = new_df['Scrap wafer'] * new_df['CPW'] * new_df['Concentration Factor']
new_df['Weekly CoNC prediction'] =  '$' + new_df['Weekly CoNC prediction'].round(2).astype(str) 

# 計算預測值（保留原始數值以便加總）
total_shipped_die_sum = summary_df['Total_shipped_die'].sum()
new_df['Weekly NCD prediction numeric'] = (
    summary_df['DPW'] * summary_df['Scrap wafer'] / total_shipped_die_sum * 100
)
new_df['Weekly CoNC prediction numeric'] = (
    new_df['Scrap wafer'] * new_df['CPW'] * new_df['Concentration Factor']
)

# 建立顯示用的 DataFrame（CPW 顯示為整數）
new_df_display = new_df.copy()
new_df_display['CPW'] = new_df_display['CPW'].round().astype(int)
new_df_display['Weekly NCD prediction'] = new_df['Weekly NCD prediction numeric'].round(2).astype(str) + '%'
new_df_display['Weekly CoNC prediction'] = '$' + new_df['Weekly CoNC prediction numeric'].round(2).astype(str) 

# 建立總和列
sum_row = {
    'DID': 'sum',
    'MDPW': '',
    'DPW': '',
    'CPW': '',
    'Concentration Factor': '',
    'Scrap wafer': new_df['Scrap wafer'].sum(),
    'Weekly NCD prediction': f"{new_df['Weekly NCD prediction numeric'].sum():.2f}%",
    'Weekly CoNC prediction': f"${new_df['Weekly CoNC prediction numeric'].sum():.2f}"
}

# 加入總和列
new_df_display = pd.concat([new_df_display, pd.DataFrame([sum_row])], ignore_index=True)

# 顯示中間的 DataFrame
st.subheader("Weekly NCD/CoNC Prediction")
st.dataframe(new_df_display[['DID', 'MPDW', 'DPW', 'CPW', 'Concentration Factor', 'Scrap wafer', 'Weekly NCD prediction', 'Weekly CoNC prediction']])


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
    'PLANNED_QDR_WAFER': summary_df['PLANNED_QDR_WAFER'].sum()
}

# 加入 sum row 到 DataFrame
summary_df = pd.concat([summary_df, pd.DataFrame([sum_row])], ignore_index=True)



# 顯示更新後的資料表
st.subheader("Baseline SQDR NCD% Summary (4RA)")
display_df = summary_df.drop(columns=['Weekly NCD prediction_raw','Scrap wafer'])
st.dataframe(display_df)

























