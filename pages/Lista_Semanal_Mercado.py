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

base['ClasseNum'] = dic_classe[base['Classe']]

base['Nota'] = ''



posicoes = [1,2,3,4,5,6,7,8,8.5,9,9.5,10,11]




st.write(base)
