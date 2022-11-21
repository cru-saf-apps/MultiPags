import streamlit as st
import pandas as pd
import openpyxl

base = pd.read_excel('DESTAQUES.xlsx',engine='openpyxl')

dic_classe = {'A':6,
              'B':5,
              'C':4,
              'D':3,
              'E':2,
              'F':1}

base['ClasseNum'] = ''

for index, row in base.iterrows():
  base['ClasseNum'][index] = dic_classe[base['Classe'][index]]
  base['Posição'][index] = float(base['Posição'][index].split(' ')[0].strip())
  
base['Nota'] = (base['Projeção'] + base['ClasseNum'])/2


posicoes = [1,2,3,4,5,6,7,8,8.5,9,9.5,10,11]

col1, col2, col3 = st.columns(3)

with col1:
  st.write(base[base.Posição==11])

with col2:
  st.write(base[base.Posição==9])

with col3:
  st.write(base[base.Posição==7])

st.write(base)
