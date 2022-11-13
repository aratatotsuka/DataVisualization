import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class Page:
    def __init__(self, df):
        self.df = df
        self.df_columns = self.df.columns
        self.df_columns_list = self.df_columns.tolist()
        if 'option' not in st.session_state:
            st.session_state["option"] = self.df_columns[0]
        if 'option2' not in st.session_state:
            st.session_state["option2"] = None
        if 'option3' not in st.session_state:
            st.session_state["option3"] = self.df_columns[0]
        st.write(st.session_state["option"])

    def home_page(self):
        st.markdown("### 入力データ")
        st.dataframe(self.df, width=None, height=None)
        st.write(self.df.describe())

    def line_chart_page(self):
        option = st.selectbox("カラムを選択してください", self.df_columns)
        st.line_chart()

    def boxplot_page(self):
        #option = st.selectbox("絞り込みたいカラムを選択してください", self.df_columns, key="option")
        #option2 = st.multiselect("ユニーク選択", self.df[st.session_state["option"]].unique(), key="option2")
        #option3 = st.selectbox("カラムを選択してください", self.df_columns, key="option3")
        option = st.selectbox("絞り込みたいカラムを選択してください", self.df_columns, index=self.df_columns_list.index(st.session_state["option"]))
        option2 = st.multiselect("ユニーク選択", self.df[st.session_state["option"]].unique(), default=st.session_state["option2"])
        option3 = st.selectbox("カラムを選択してください", self.df_columns, index=self.df_columns_list.index(st.session_state["option3"]))
        st.session_state['option'] = option
        st.session_state['option2'] = option2
        st.session_state['option3'] = option3
        a = list()
        if option2:
            for i in option2:
                a.append(self.df[self.df[option]==i][option3])
            fig, ax = plt.subplots()
            plt.boxplot(a, labels=option2)
            st.pyplot(fig)
    