import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from page import Page

page_list = ["ホーム", "箱ひげ図"]

st.title("Data Visualization")

# 以下をサイドバーに表示
st.sidebar.markdown("### 機械学習に用いるcsvファイルを入力してください")
# ファイルアップロード
uploaded_files = st.sidebar.file_uploader("Choose a CSV file", accept_multiple_files= False)

# ページ切り替え
page_status = st.sidebar.radio("ページ選択", page_list)

if uploaded_files:
    df = pd.read_csv(uploaded_files, header=0)
    st.session_state["dv_page"] = Page(df)

match page_status:
    case "ホーム":
        st.session_state["dv_page"].home_page()
    case "箱ひげ図":
        st.session_state["dv_page"].boxplot_page()
    case _:
        st.write("ファイルをアップロードしてください")