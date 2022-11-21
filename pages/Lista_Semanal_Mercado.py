import streamlit as st
import pandas as pd
import openpyxl

st.set_page_config(layout="wide")


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
base['Nota'] = base['Nota'].astype(float)

posicoes = [1,2,3,4,5,6,7,8,8.5,9,9.5,10,11]

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

# Display a static table


col11, col9, col7 = st.columns(3)

with col11:
  st.subheader('Ext. Esquerdo')
  st.table(base[base.Posição==11].nlargest(10,'Nota')[['Nome','Clube','Data de Nascimento']])

with col9:
  st.subheader('Centroavante')
  st.table(base[base.Posição==9].nlargest(10,'Nota')[['Nome','Clube','Data de Nascimento']])

with col7:
  st.subheader('Ext. Direito')
  st.table(base[base.Posição==7].nlargest(10,'Nota')[['Nome','Clube','Data de Nascimento']])

  
col10, col9meio = st.columns(2)

with col10:
  st.subheader('Meia')
  st.table(base[base.Posição == 10].nlargest(10,'Nota')[['Nome','Clube','Data de Nascimento']])
  
with col9meio:
  st.subheader('Segundo atacante')
  st.table(base[base.Posição==9.5].nlargest(10,'Nota')[['Nome','Clube','Data de Nascimento']])
  
  
col8meio, col5, col8 = st.columns(3)

with col8meio:
  st.subheader('Médio Ofensivo')
  st.table(base[base.Posição == 8.5].nlargest(10,'Nota')[['Nome','Clube','Data de Nascimento']])
  
with col5:
  st.subheader('Médio Defensivo')
  st.table(base[base.Posição == 5].nlargest(10,'Nota')[['Nome','Clube','Data de Nascimento']])
  
with col8:
  st.subheader('Box to Box')
  st.table(base[base.Posição == 8].nlargest(10,'Nota')[['Nome','Clube','Data de Nascimento']])

col6, col3, col4, col2 = st.columns(4)

with col6:
  st.subheader('Lat. Esquerdo')
  st.table(base[base.Posição == 6].nlargest(10,'Nota')[['Nome','Clube','Data de Nascimento']])

with col3:
  st.subheader('Zag. Esquerdo')
  st.table(base[base.Posição == 3].nlargest(10,'Nota')[['Nome','Clube','Data de Nascimento']])
  
with col4:
  st.subheader('Zag. Direito')
  st.table(base[base.Posição == 4].nlargest(10,'Nota')[['Nome','Clube','Data de Nascimento']])
  
with col2:
  st.subheader('Lat. Direito')
  st.table(base[base.Posição == 2].nlargest(10,'Nota')[['Nome','Clube','Data de Nascimento']])
  
  
  
