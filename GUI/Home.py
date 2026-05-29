#! /Work1/HOME/eonebi/anaconda3/envs/streamlit_env/bin/python3

import streamlit as st

st.set_page_config(
    page_title='Virtual Colony Reading'
)


st.title("Virtual Colony Reading")
st.caption("EONE Laboratories Microbiome")
st.write("왼쪽 사이드바에서 원하는 메뉴(Home 또는 PlateView)를 선택하세요!")
st.divider()

st.markdown("Virtual Colony Reading is about a method and system for virtually reproducing and visualizing microbial community data obtained by NGS(Next-Generation-Sequencing) like a colony distribution of an actual culture dish.")

