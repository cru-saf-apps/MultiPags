import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(layout="wide")


negoc = pd.read_excel('NEGOCIAÇÕES.xlsx',engine='openpyxl')
hist = pd.read_excel('HISTÓRICO.xlsx',engine='openpyxl')
hist['DATA HISTÓRICO'] = pd.to_datetime(hist['DATA HISTÓRICO']).dt.date


df_hist = pd.DataFrame()

for jogador in negoc.ID:
  
  hist_jog = hist[hist['ID ATLETA'] == jogador].reset_index(drop=True)
  comp = len(hist_jog)
  
  st.title(hist_jog[hist_jog['ID ATLETA']==jogador]['ATLETA'].tolist()[0])
  
  t = 1
  while t <= comp:
    
    st.subheader(hist_jog['DATA HISTÓRICO'][t-1])
    st.write(hist_jog['DESCRIÇÃO HISTÓRICO'][t-1])

    t+=1



