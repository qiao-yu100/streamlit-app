import streamlit as st
import pandas as pd

# 初始資料
data = {
    'TN': ['TN1', 'TN2', 'TN3'],
    'p': [0, 0, 0],
    'q': [0, 0, 0]
}
df = pd.DataFrame(data)

# 建立輸入介面
st.title("互動式資料輸入與計算")
st.write("請輸入每一列的 p 值，系統會自動計算 q = p * 2")

for i in range(len(df)):
    df.at[i, 'p'] = st.number_input(f"{df.at[i, 'TN']} 的 p 值", value=df.at[i, 'p'], key=f"p_{i}")
    df.at[i, 'q'] = df.at[i, 'p'] * 2  # 這裡可以改成你想要的邏輯

# 顯示結果
st.subheader("計算結果")
st.dataframe(df)
