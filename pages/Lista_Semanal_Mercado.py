import streamlit as st
import pandas as pd

base = pd.read_excel('DESTAQUES.xlsx',engine=openpyxl)

st.write(base)
