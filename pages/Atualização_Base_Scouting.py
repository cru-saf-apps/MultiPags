import streamlit as st
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from fpdf import FPDF
import base64
from gspread_pandas import Spread,Client
from google.oauth2 import service_account
import time
import datetime as dt


@st.cache(ttl=6000)
def load_spreadsheet(spreadsheet_name):
    worksheet = sh.worksheet(spreadsheet_name)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

def update_spreadsheet(spreadsheet_name, df):
    spread.df_to_sheet(df,sheet = spreadsheet_name,index=False,replace=True)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

headers = {'User-Agent': 
           'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'}

client = Client(scope = scope, creds = credentials)




spreadsheet_name = "BASE CLUBES"
spread = Spread(spreadsheet_name, client = client)
sh = client.open(spreadsheet_name)
base_clubes = load_spreadsheet(spreadsheet_name)

@st.cache
def busca_clubes():
    ano = '2022'

    ligas = ['BRA1','BRA2','BRA3','BRA4','MEXA','AR1N','URU1','CLPD','COLP',
             'PR1A','VZ1L','PER1','BO1C']

    lista_nome = []
    lista_foto = []
    lista_liga = []

    for liga in ligas:

        url = 'https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/startseite/wettbewerb/'+liga+'/plus/?saison_id='+ano

        page = requests.get(url, headers=headers)

        soup = bs(page.content,'html.parser')

        nomes = soup.find_all('td',{'class':'no-border-links hauptlink'})

        for nome in nomes:
            lista_nome.append(nome.find('a').text)

            id_clube = nome.find('a').get('href').split('/')[4]

            lista_foto.append('https://tmssl.akamaized.net/images/wappen/head/'+id_clube+'.png')

            lista_liga.append(liga)

        time.sleep(2)
        st.write(liga+ano)


    df_clubes = pd.DataFrame({'Clube':lista_nome,'LinkFoto':lista_foto,'Liga':lista_liga})    

    dic_pais = {'BRA1':'Brasil Série A','BRA2':'Brasil Série B','AR1N':'Argentina 1ª Div','URU1':'Uruguai 1ª Div',
                'CLPD':'Chile 1ª Div','COLP':'Colombia 1ª Div','BRA3':'Brasil Série C','MEXA':'Mexico 1ª Div',
                'BRA4':'Brasil Série D','PR1A':'Paraguai 1ª Div','VZ1L':'Venezuela 1ª Div',
                'PER1':'Peru 1ª Div','BO1C':'Bolivia 1ª Div'}

    for index, row in df_clubes.iterrows():
        df_clubes.Liga[index] = dic_pais[df_clubes.Liga[index]]

    for index, row in df_clubes.iterrows():
        if df_clubes.LinkFoto[index].split('/')[-1].split('.')[0].isdigit():
            continue
        else:
            df_clubes = df_clubes.drop(index)

    df_clubes['IDClube'] = ''
    for index, row in df_clubes.iterrows():
        df_clubes.IDClube[index] = df_clubes.LinkFoto[index].split('/')[-1].split('.')[0]

    df_clubes = df_clubes.assign(DataAtualização = dt.date.today().strftime("%d/%m/%Y"))

    df_clubes = df_clubes.drop_duplicates('IDClube').reset_index(drop=True)
    
    return df_clubes

df_clubes = busca_clubes()

st.write(df_clubes)


base_atualizada = pd.concat([base_clubes,df_clubes])

base_atualizada.sort_values(by='DataAtualização',ascending=False)

base_atualizada.drop_duplicates('IDClube')

   
update_spreadsheet(spreadsheet_name,base_atualizada)






