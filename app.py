import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from page import Page

page_list = ["ホーム", "棒グラフ", "箱ひげ図"]
st.set_page_config(
    page_title="Data Visualization",
    layout="wide")

# 以下をサイドバーに表示
st.sidebar.markdown("### 機械学習に用いるcsvファイルを入力してください")
# ファイルアップロード
uploaded_files = st.sidebar.file_uploader("Choose a CSV file", accept_multiple_files= False)

# ページ切り替え
page_status = st.sidebar.radio("ページ選択", page_list)

if uploaded_files:
    st.session_state["file"] = pd.read_csv(uploaded_files, header=0)
    dv_page = Page(st.session_state["file"])
if "file" in st.session_state:
    match page_status:
        case "ホーム":
            dv_page.home_page()
        case "棒グラフ":
            dv_page.bar_chart_page()
        case "箱ひげ図":
            dv_page.boxplot_page()
else:
    st.write("ファイルをアップロードしてください")