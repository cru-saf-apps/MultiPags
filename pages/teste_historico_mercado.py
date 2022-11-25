import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64
from gspread_pandas import Spread,Client
from google.oauth2 import service_account


@st.cache(ttl=30)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = Client(scope = scope, creds = credentials)

spreadsheet_name = "HISTÓRICO"

spread = Spread(spreadsheet_name, client = client)

st.write(spread.url)


sh = client.open(spreadsheet_name)

def load_spreadsheet(spreadsheet_name):
    worksheet = sh.worksheet(spreadsheet_name)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

hist = load_spreadsheet(spreadsheet_name)



hist.loc[len(hist)] = ['teste','teste','teste','teste','teste','teste','teste','teste']
st.write(hist)
             
def update_spreadsheet(spreadsheet_name, df):
    spread.df_to_sheet(df,sheet = spreadsheet_name,index=False,replace=True)
   
update_spreadsheet(spreadsheet_name,hist)






    
    
hist['DATA HISTÓRICO'] = pd.to_datetime(hist['DATA HISTÓRICO']).dt.date
negoc = negoc.sort_values(by='ATLETA')

jogadores = st.multiselect('Selecione os jogadores que deseja ver o histórico:',pd.unique(negoc.ATLETA))

negoc = negoc[negoc.ATLETA.isin(jogadores)]

pdf = FPDF()
pdf.add_page()

for jogador in negoc.ID:
  try:
    hist_jog = hist[hist['ID ATLETA'] == jogador].reset_index(drop=True)
    comp = len(hist_jog)

    pdf.set_font('Arial','B',16)
    pdf.cell(40, 10, hist_jog[hist_jog['ID ATLETA']==jogador]['ATLETA'].tolist()[0],ln=1)

    t = 1
    while t <= comp:

      pdf.set_font('Arial','B',12)
      pdf.cell(40, 10, str(hist_jog['DATA HISTÓRICO'][t-1]),ln=1)

      pdf.set_font('Arial','',10)
      pdf.multi_cell(180, 10,hist_jog['DESCRIÇÃO HISTÓRICO'][t-1])

      t+=1
  except:
    continue

export_as_pdf = st.button("Exportar")

if export_as_pdf:
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), "Histórico de Negociações")
    st.markdown(html, unsafe_allow_html=True)
