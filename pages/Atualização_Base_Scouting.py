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

st.write(len(base_clubes), " clubes carregados.")

def busca_clubes():
    ano = '2022'

    ligas = ['BRA1','BRA2','BRA3','BRA4','MEXA','AR1N','URU1','CLPD','COLP',
             'PR1A','VZ1L','PER1','BO1C','GB1']

    lista_nome = []
    lista_foto = []
    lista_liga = []

    for liga in ligas:

        url = 'https://www.transfermarkt.com.br/campeonato-brasileiro-serie-a/startseite/wettbewerb/'+liga+'/plus/?saison_id='+ano

        page = requests.get(url, headers=headers)

        soup = bs(page.content,'html.parser')

        nomes = soup.find_all('td',{'class':'no-border-links hauptlink'})

        for nome in nomes:
            lista_nome.append(str(nome.find('a').text))

            id_clube = str(nome.find('a').get('href').split('/')[4])

            lista_foto.append(str('https://tmssl.akamaized.net/images/wappen/head/'+id_clube+'.png'))

            lista_liga.append(str(liga))

        time.sleep(2)
        

    df_clubes = pd.DataFrame({'Clube':lista_nome,'LinkFoto':lista_foto,'Liga':lista_liga})    

    dic_pais = {'BRA1':'Brasil Série A','BRA2':'Brasil Série B','AR1N':'Argentina 1ª Div','URU1':'Uruguai 1ª Div',
                'CLPD':'Chile 1ª Div','COLP':'Colombia 1ª Div','BRA3':'Brasil Série C','MEXA':'Mexico 1ª Div',
                'BRA4':'Brasil Série D','PR1A':'Paraguai 1ª Div','VZ1L':'Venezuela 1ª Div',
                'PER1':'Peru 1ª Div','BO1C':'Bolivia 1ª Div',
                'GB1':'Inglaterra Premier League'}

    for index, row in df_clubes.iterrows():
        df_clubes.Liga[index] = str(dic_pais[df_clubes.Liga[index]])

    for index, row in df_clubes.iterrows():
        if df_clubes.LinkFoto[index].split('/')[-1].split('.')[0].isdigit():
            continue
        else:
            df_clubes = df_clubes.drop(index)

    df_clubes['IDClube'] = ''
    for index, row in df_clubes.iterrows():
        df_clubes.IDClube[index] = df_clubes.LinkFoto[index].split('/')[-1].split('.')[0]

    df_clubes['Data Atualização'] = str(dt.date.today().strftime("%d/%m/%Y"))

    df_clubes = df_clubes.drop_duplicates('IDClube').reset_index(drop=True)
    
    df_clubes = df_clubes.astype(dtype={'Clube': 'string','LinkFoto':'string','Liga':'string','IDClube':'int64','Data Atualização':'datetime64[ns]'})
    
    return df_clubes


spreadsheet_name = "BASE ELENCOS"
spread = Spread(spreadsheet_name, client = client)
sh = client.open(spreadsheet_name)
base_elencos = load_spreadsheet(spreadsheet_name)


st.write(len(base_elencos), " jogadores carregados.")

def busca_elencos():

    df_elencos = pd.DataFrame()

    for index, row in base_clubes.iterrows():
        id_clube = base_clubes.LinkFoto[index].split('/')[-1].split('.')[0]
        clube = base_clubes.Clube[index]
        pais_clube = base_clubes['Liga'][index]

        link = 'https://www.transfermarkt.com.br/se-palmeiras/kader/verein/'+id_clube+'/plus/1/galerie/0?saison_id=2021'

        page = requests.get(link, headers=headers)

        soup = bs(page.content,'html.parser')

        elenco = soup.find('table',{'class':'items'})

        if elenco is None:
            continue

        tabelas_inline = elenco.find_all('table',{'class':'inline-table'})

        lista_pag = []
        lista_nome = []
        lista_pos = []
        lista_fotos = []
        for tabela in tabelas_inline:
            tds = tabela.find_all('td')

            foto = str(tds[0].find('img').get('data-src'))
            lista_fotos.append(foto)

            nome = str(tds[1].text.strip())
            lista_nome.append(nome)

            pag = str('www.transfermarkt.com.br'+tds[1].find('a').get('href'))
            lista_pag.append(pag)

            pos = str(tds[2].text.strip())
            lista_pos.append(pos)


        linhas = elenco.find_all('tr')[1:]
        lista_ranges = list(range(0,len(linhas),3))

        lista_datanasc = []
        lista_paisnasc = []
        lista_altura = []
        lista_pe = []
        lista_contrato = []

        for valor in lista_ranges:
            tds = linhas[valor].find_all('td')

            data_nasc = str(tds[5].text.split('(')[0].strip())
            pais_nasc = str(tds[6].find('img').get('title'))
            try:
                altura = str(int(tds[7].text.split('m')[0].replace(',','')))
            except:
                altura = '-'
            pe = str(tds[8].text)
            contrato = str(tds[11].text)

            lista_datanasc.append(data_nasc)
            lista_paisnasc.append(pais_nasc)
            lista_altura.append(altura)
            lista_pe.append(pe)
            lista_contrato.append(contrato)

        elenco_clube = pd.DataFrame({'Clube':clube,
                                     'Liga':pais_clube,
                                     'Foto':lista_fotos,
                                     'Nome':lista_nome,
                                     'Posição':lista_pos,
                                     'Data Nascimento':lista_datanasc,
                                     'Nacionalidade':lista_paisnasc,
                                     'Altura':lista_altura,
                                     'Pé':lista_pe,
                                     'Contrato':lista_contrato,
                                     'Link Transfermarkt':lista_pag,
                                     'Data Atualização':dt.date.today().strftime("%d/%m/%Y")
        } 
        )

        df_elencos = pd.concat([df_elencos,elenco_clube])
        
        time.sleep(1)
    
    df_elencos = df_elencos.reset_index(drop=True)

    df_elencos['ID'] = ''
    for index, row in df_elencos.iterrows():
        df_elencos['ID'][index] = df_elencos['Link Transfermarkt'][index].split('/')[4]
        
    df_elencos = df_elencos.astype(dtype={'Clube':'string','Liga':'string','Foto':'string','Nome':'string','Posição':'string','Data Nascimento':'datetime64[ns]','Nacionalidade':'string','Altura':'string','Pé':'string','Contrato':'datetime64[ns]','Link Transfermarkt':'string','Data Atualização':'datetime64[ns]'})
    
    return df_elencos


base_clubes = base_clubes.astype(dtype={'Clube': 'string','LinkFoto':'string','Liga':'string','Data Atualização':'datetime64[ns]'})
base_elencos = base_elencos.astype(dtype={'Clube':'string','Liga':'string','Foto':'string','Nome':'string','Posição':'string','Data Nascimento':'datetime64[ns]','Nacionalidade':'string','Altura':'string','Pé':'string','Contrato':'datetime64[ns]','Link Transfermarkt':'string','Data Atualização':'datetime64[ns]'})

st.write(base_clubes.dtypes)                 

botao_atualizar_clubes = st.button('Atualizar Clubes')

if botao_atualizar_clubes:
    
    with st.spinner('Buscando clubes'):
        df_clubes = busca_clubes()

        base_clubes_atualizada = pd.concat([base_clubes,df_clubes])

        base_clubes_atualizada = base_clubes_atualizada.sort_values(by='Data Atualização',ascending=True)

        base_clubes_atualizada.drop_duplicates(subset=['IDClube'],keep='first',inplace=True)
        
        spreadsheet_name = "BASE CLUBES"
        spread = Spread(spreadsheet_name, client = client)
        sh = client.open(spreadsheet_name)

        update_spreadsheet(spreadsheet_name,base_clubes_atualizada)
    
    st.write('Clubes atualizados')

botao_atualizar_jogs = st.button('Atualizar Jogadores')

if botao_atualizar_jogs:
    
    with st.spinner('Buscando jogadores'):
        df_elencos = busca_elencos()

        base_elencos_atualizada = pd.concat([base_elencos,df_elencos])

        base_elencos_atualizada = base_elencos_atualizada.sort_values(by='Data Atualização',ascending=True)

        base_elencos_atualizada = base_elencos_atualizada.drop_duplicates('ID',keep='first',inplace=True)

        spreadsheet_name = "BASE ELENCOS"
        spread = Spread(spreadsheet_name, client = client)
        sh = client.open(spreadsheet_name)

        update_spreadsheet(spreadsheet_name,base_elencos_atualizada)

    st.write('Elencos atualizados')
    
    





