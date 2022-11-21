import streamlit as st
import pandas as pd

base = pd.read_excel('DESTAQUES.xlsx')

st.write(base)
