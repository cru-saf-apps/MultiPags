import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(layout="wide")


negoc = pd.read_excel('NEGOCIAÇÕES.xlsx',engine='openpyxl')
hist = pd.read_excel('HISTÓRICO.xlsx',engine='openpyxl')


df_hist = pd.DataFrame()

for jogador in negoc.ID:
  
  aux_df = pd.DataFrame(columns = ['Atleta','Posição','Clube','Ano'])
  
  aux_df['Atleta'][0] = negoc[negoc.ID == jogador]['ATLETA']
  aux_df['Posição'][0] = negoc[negoc.ID == jogador]['POSIÇÃO']
  aux_df['Clube'][0] = negoc[negoc.ID == jogador]['CLUBE']
  aux_df['Ano'][0] = negoc[negoc.ID == jogador]['ANO']
  
  hist_jog = hist[hist['ID ATLETA'] == jogador].reset_index(drop=True)
  comp = len(hist_jog)
  
  t = 1
  while t <= comp:
    aux_df['Atleta'][t] = hist_jog['DESCRIÇÃO HISTÓRICO'][t-1]
  
  
  df_hist = pd.concat([df_hist,aux_df])

st.write(df_hist)  

st.write(hist.sort_values(by=['ID ATLETA','DATA HISTÓRICO']))
