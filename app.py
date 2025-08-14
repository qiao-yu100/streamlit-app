import streamlit as st
import pandas as pd

# 讀取資料
summary_df = pd.read_csv("summary_wip_prediction.csv")

# 計算 Scrap wafer 與 Weekly NCD prediction（略）

# 加入 sum row（略）

# 顯示資料表
st.subheader("Baseline SQDR NCD% Summary (4RA)")
display_df = summary_df.drop(columns=['Weekly NCD prediction_raw'])

# 使用 data_editor 並設定 column_config
st.data_editor(
    display_df,
    column_config={
        "WIP Projection": st.column_config.Column(
            "WIP Projection",
            help="WIP 預測",
            disabled=True,
            width="medium",
            style={"backgroundColor": "#D6EAF8"}
        ),
        "Scrap wafer": st.column_config.Column(
            "Scrap wafer",
            help="報廢晶圓數",
            disabled=True,
            width="medium",
            style={"backgroundColor": "#D6EAF8"}
        ),
        "Weekly NCD prediction": st.column_config.Column(
            "Weekly NCD prediction",
            help="每週 NCD 預測",
            disabled=True,
            width="medium",
            style={"backgroundColor": "#D6EAF8"}
        ),
    },
    disabled=True,
    hide_index=True
)
























