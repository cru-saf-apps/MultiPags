import streamlit as st
import pandas as pd
import openpyxl
from fpdf import FPDF
import base64
from google.oauth2 import service_account
from gsheetsdb import connect


@st.cache(ttl=30)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets"
    ]
)


conn = connect(credentials = credentials)

hist_url = st.secrets["private_gsheets_url"].historico
rows = run_query(f'SELECT * FROM "{hist_url}"')

hist = pd.DataFrame(columns = ['ID ATLETA',	'ID HISTÓRICO',	'ATLETA',
                               'POSIÇÃO',	'CLUBE',	'DATA HISTÓRICO',
                               'DESCRIÇÃO HISTÓRICO',	'RESPONSÁVEL CEC'])


conn.execute(f'INSERT INTO "{hist_url}" VALUES("{hist.loc[len(hist)]}")',
             headers=1
            )

# Print results.
for row in rows:
    hist.loc[len(hist)] = row

negoc_url = st.secrets["private_gsheets_url"].negociacoes
rows = run_query(f'SELECT * FROM "{negoc_url}"')

negoc = pd.DataFrame(columns = [	'ID','ATLETA',	'ANO','CLASSE',
                                'POSIÇÃO',	'CLUBE','AGENTE','STATUS'])
for row in rows:
    negoc.loc[len(negoc)] = row
    
    
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
