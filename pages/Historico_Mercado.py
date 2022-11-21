import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(layout="wide")


negoc = pd.read_excel('NEGOCIAÇÕES.xlsx',engine='openpyxl')
hist = pd.read_excel('HISTÓRICO.xlsx',engine='openpyxl')


df_hist = pd.DataFrame()

for jogador in negoc.ID:
  
  dic_aux = {'Atleta':negoc[negoc.ID == jogador]['ATLETA'],
             'Posição'negoc[negoc.ID == jogador]['POSIÇÃO'],
             'Clube':negoc[negoc.ID == jogador]['CLUBE'],
             'Ano':negoc[negoc.ID == jogador]['ANO']}
  
  aux_df = pd.DataFrame(dic_aux)
  
  hist_jog = hist[hist['ID ATLETA'] == jogador].reset_index(drop=True)
  comp = len(hist_jog)
  
  t = 1
  while t <= comp:
    aux_df.loc[len(aux_df)] = hist_jog['DESCRIÇÃO HISTÓRICO'][t-1]

  df_hist = pd.concat([df_hist,aux_df])

st.write(df_hist)  

st.write(hist.sort_values(by=['ID ATLETA','DATA HISTÓRICO']))
