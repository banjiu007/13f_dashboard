import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.gini import gini_coefficient

st.set_page_config(page_title="13F Dashboard", layout="wide")

# ------------------ 数据加载 ------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/sample_13f_data.csv")
    return df

df = load_data()

# ------------------ 侧边栏筛选 ------------------
st.sidebar.title("筛选器")
quarter = st.sidebar.selectbox("选择季度", sorted(df['quarter'].unique(), reverse=True))
sector = st.sidebar.multiselect("选择行业", sorted(df['sector'].unique()))
institution = st.sidebar.multiselect("选择机构", sorted(df['institution'].unique()))
metric = st.sidebar.radio("显示指标", ['market_value', 'share_count', 'holding_pct'])

# ------------------ 数据过滤 ------------------
filtered = df[df['quarter'] == quarter]
if sector:
    filtered = filtered[filtered['sector'].isin(sector)]
if institution:
    filtered = filtered[filtered['institution'].isin(institution)]

# ------------------ 主图表 ------------------
st.title(f"13F 持仓分析 - {quarter}")
col1, col2 = st.columns([2, 1])

with col1:
    sector_df = filtered.groupby('sector')[metric].sum().reset_index()
    fig_bar = px.bar(sector_df, x='sector', y=metric, title="行业持仓总览")
    selected_sector = st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    top_stocks = filtered.groupby('stock')[metric].sum().nlargest(10).reset_index()
    fig_pie = px.pie(top_stocks, names='stock', values=metric, title="Top10 股票占比")
    st.plotly_chart(fig_pie, use_container_width=True)

# ------------------ 表格与集中度 ------------------
st.subheader("持仓明细表")
st.dataframe(filtered.sort_values(by=metric, ascending=False))

st.markdown("---")
col1, col2 = st.columns(2)
with col1:
    gini = gini_coefficient(filtered[metric].values)
    st.metric("集中度 (Gini 系数)", gini)

with col2:
    st.download_button("导出筛选结果", filtered.to_csv(index=False), file_name="filtered_13f.csv")