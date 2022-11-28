import streamlit as st
import pandas as pd
from gspread_pandas import Spread,Client
from google.oauth2 import service_account

st.set_page_config(layout="wide")

def load_spreadsheet(spreadsheet_name):
    worksheet = sh.worksheet(spreadsheet_name)
    df = pd.DataFrame(worksheet.get_all_records())
    return df
  
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = Client(scope = scope, creds = credentials)

spreadsheet_name = "DESTAQUES"
spread = Spread(spreadsheet_name, client = client)
sh = client.open(spreadsheet_name)
base = load_spreadsheet(spreadsheet_name)


def path_to_image_html(path):
    return '<img src="' + path + '" width="60" >'

st.markdown(
    base.to_html(escape=False, formatters=dict(Foto=path_to_image_html)),
    unsafe_allow_html=True,
)


st.write(base)

dic_classe = {'A':6,
              'B':5,
              'C':4,
              'D':3,
              'E':2,
              'F':1}

posicoes = [1,2,3,4,5,6,7,8,8.5,9,9.5,10,11]

hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)



col11, col9, col7 = st.columns(3)

with col11:
  st.subheader('Ext. Esquerdo')
  st.table(base[base.Posição==11][['Nome','Clube','Data de Nascimento']])

with col9:
  st.subheader('Centroavante')
  st.table(base[base.Posição==9][['Nome','Clube','Data de Nascimento']])

with col7:
  st.subheader('Ext. Direito')
  st.table(base[base.Posição==7][['Nome','Clube','Data de Nascimento']])

  
col10, col9meio = st.columns(2)

with col10:
  st.subheader('Meia')
  st.table(base[base.Posição == 10][['Nome','Clube','Data de Nascimento']])
  
with col9meio:
  st.subheader('Segundo atacante')
  st.table(base[base.Posição==9.5][['Nome','Clube','Data de Nascimento']])
  
  
col8meio, col5, col8 = st.columns(3)

with col8meio:
  st.subheader('Médio Ofensivo')
  st.table(base[base.Posição == 8.5][['Nome','Clube','Data de Nascimento']])
  
with col5:
  st.subheader('Médio Defensivo')
  st.table(base[base.Posição == 5][['Nome','Clube','Data de Nascimento']])
  
with col8:
  st.subheader('Box to Box')
  st.table(base[base.Posição == 8][['Nome','Clube','Data de Nascimento']])

col6, col3, col4, col2 = st.columns(4)

with col6:
  st.subheader('Lat. Esquerdo')
  st.table(base[base.Posição == 6][['Nome','Clube','Data de Nascimento']])

with col3:
  st.subheader('Zag. Esquerdo')
  st.markdown(
    base[base.Posição == 'Zagueiro'][['Foto','Nome','Clube']].to_html(escape=False, formatters=dict(Foto=path_to_image_html)),
    unsafe_allow_html=True,
  )
  st.write(base[base.Posição == 'Zagueiro'][['Foto','Nome','Clube']])
  
with col4:
  st.subheader('Zag. Direito')
  st.table(base[base.Posição == 4][['Nome','Clube','Data de Nascimento']])
  
with col2:
  st.subheader('Lat. Direito')
  st.table(base[base.Posição == 2][['Nome','Clube','Data de Nascimento']])
  
  
  
