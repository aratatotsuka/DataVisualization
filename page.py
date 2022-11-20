import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import io

class Page:
    def __init__(self, df):
        mplstyle.use('fast')
        self.df = df
        self.df_columns = self.df.columns
        self.df_columns_list = self.df_columns.tolist()
        self.__init_session_state()

    def __init_session_state(self):
        if 'refine_column' not in st.session_state:
            st.session_state["refine_column"] = self.df_columns[0]
        if 'option2' not in st.session_state:
            st.session_state["option2"] = None
        if 'main_column' not in st.session_state:
            st.session_state["main_column"] = self.df_columns[0]
        if 'slide' not in st.session_state:
            st.session_state["slide"] = 1.5
        if 'visual_button_state' not in st.session_state:
            st.session_state["visual_button_state"] = False
        if 'filter_state' not in st.session_state:
            st.session_state["filter_state"] = False
        self.__init_session_state_bar_chart()
    
    def __init_session_state_bar_chart(self):
        if 'bc_main_column' not in st.session_state:
            st.session_state["bc_main_column"] = self.df_columns[0]
        if 'bc_visual_button_state' not in st.session_state:
            st.session_state["bc_visual_button_state"] = False

    def __init_session_state_boxplot(self):
        pass

    def home_page(self):
        st.markdown("### 入力データ")
        st.dataframe(self.df, width=None, height=None)
        st.write(self.df.describe())

    def line_chart_page(self):
        option = st.selectbox("カラムを選択してください", self.df_columns)
        st.line_chart()
    
    def bar_chart_page(self):
        usage_rule = st.radio("使用方法", ("カテゴリ変数の個数",))
        if usage_rule == "カテゴリ変数の個数":
            rule = st.radio("選択", ("単一カテゴリ変数の個数を表示", "別カテゴリ変数ごとに個数を表示"))
            bc_main_column = st.selectbox("カラムを選択してください", self.df_columns, key="bc_main_column")
            if rule == "単一カテゴリ変数の個数を表示":
                st.bar_chart(self.df[bc_main_column].value_counts(sort=True))
            if rule == "別カテゴリ変数ごとに個数を表示":
                option2 = st.selectbox("絞り込みたいカラムを選択してください", self.df_columns)
                sort_columns = sorted(self.df[bc_main_column].unique())
                sharey = st.checkbox("y軸を揃える")
                fig, ax = plt.subplots(4, 3, tight_layout=True, figsize=(25.0, 50.0), sharey=sharey)
                visual_state = st.checkbox("グラフの表示", key="bc_visual_button_state")
                if visual_state:
                    for index, op in enumerate(sorted(self.df[option2].unique())):
                        dic_value_counts = self.df[self.df[option2]==op][bc_main_column].value_counts().to_dict()
                        sort_values  = [0 if column not in dic_value_counts else dic_value_counts[column] for column in sort_columns]
                        ax[index//3, index%3].bar(sort_columns, sort_values)
                        ax[index//3, index%3].set_title(op)
                        ax[index//3, index%3].tick_params(labelrotation=90)
                    st.pyplot(fig)
                    self.__download_button("bar_chart", fig)

    def boxplot_page(self):
        main_column = st.selectbox("カラムを選択してください", self.df_columns, key="main_column")
        slide = st.slider("外れ値の値を設定してください。", 0.0, 5.0, 1.5, step=0.1, key="slide")
        filter_state = st.checkbox("フィルタあり/なし", key="filter_state")
        if filter_state:
            refine_column = st.selectbox("絞り込みたいカラムを選択してください", self.df_columns, key="refine_column")
            option2 = st.multiselect("ユニーク選択", self.df[refine_column].unique(), key="option2", default=self.df[refine_column].unique())
        visual_state = st.checkbox("グラフの表示", key="visual_button_state")
        data = list()
        labels = list()
        if visual_state:
            if not filter_state:
                data.append(self.df[(self.df[main_column].notna())][main_column])
                labels.append(main_column)
            elif filter_state and option2:
                for i in option2:
                    data.append(self.df[(self.df[refine_column]==i) & (self.df[main_column].notna())][main_column])
                labels = option2
            fig, ax = plt.subplots()
            st.write(data)
            plt.boxplot(data, labels=labels, whis=slide)
            st.pyplot(fig)
            self.__download_button("boxplot", fig)
    
    def __download_button(self, filename, fig):
        fn = filename + '.png'
        img = io.BytesIO()
        fig.savefig(img, format='png')
 
        btn = st.download_button(
            label="Download image",
            data=img,
            file_name=fn,
            mime="image/png"
        )
    