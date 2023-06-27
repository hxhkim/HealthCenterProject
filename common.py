import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def get_data():
    data = pd.read_csv("./hospital.csv", encoding='cp949')
    return data

def page_config():
    st.set_page_config(
        page_title="Health Centers  in Gyeonggi",
        page_icon="🏥",
    )