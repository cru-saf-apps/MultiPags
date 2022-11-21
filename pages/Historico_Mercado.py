import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(layout="wide")


negoc = pd.read_excel('NEGOCIAÇÕES.xlsx',engine='openpyxl')
hist = pd.read_excel('HISTÓRICO.xlsx',engine='openpyxl')

st.write(hist.sort_values(by=['ID ATLETA','DATA HISTÓRICO']))
