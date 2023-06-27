# pip install streamlit
# streamlit hello
# streamlit run app.py
import streamlit as st
import common

common.page_config()

st.title("Health Centers  in Gyeonggi")
st.caption("""
"응급의료기관 및 응급의료지원센터 현황" 데이터셋:
경기도 내 응급의료기관 및 응급의료지원센터 현황입니다.
URL: https://data.gg.go.kr/portal/data/service/selectServicePage.do?page=1&rows=10&sortColumn=&sortDirection=&infId=MB714IBPDSE5OPNIMW0V27143432&infSeq=1&order=&loc=&HOSPTL_NM_CENTER_NM=&REFINE_ROADNM_ADDR=&REFINE_LOTNO_ADDR=
""")
st.image("img/map.jpg")



