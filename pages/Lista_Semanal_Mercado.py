import streamlit as st
import pandas as pd
import openpyxl

base = pd.read_excel('DESTAQUES.xlsx',engine='openpyxl')

st.write(base)
