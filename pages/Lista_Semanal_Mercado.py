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

base['Nota'] = (base['Projeção'] + base['ClasseNum'])/2


posicoes = [1,2,3,4,5,6,7,8,8.5,9,9.5,10,11]




st.write(base)
