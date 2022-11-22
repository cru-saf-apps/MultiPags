import streamlit as st
from google.oauth2 import service_account
from gsheetsdb import connect
import pandas as pd

@st.cache(ttl=600)
def run_query(query):
    rows = conn.execute(query, headers=1)
    rows = rows.fetchall()
    return rows

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

# Perform SQL query on the Google Sheet.
# Uses st.cache to only rerun when the query changes or after 10 min.


sheet_url = st.secrets["private_gsheets_url"].historico
rows = run_query(f'SELECT * FROM "{sheet_url}"')

hist = pd.DataFrame(columns = ['ID ATLETA',	'ID HISTÓRICO',	'ATLETA',
                               'POSIÇÃO',	'CLUBE',	'DATA HISTÓRICO',
                               'DESCRIÇÃO HISTÓRICO',	'RESPONSÁVEL CEC'])
# Print results.
for row in rows:
    hist.loc[len(hist)] = row

st.write(hist)



sheet_url = st.secrets["private_gsheets_url"].negociacoes
rows = run_query(f'SELECT * FROM "{sheet_url}"')

negoc = pd.DataFrame(columns = ['PRIORIDAD',	'ID','ATLETA',	'ANO',
                                'POSIÇÃO',	'CLUBE',	'RESPONSÁVEL CEC',
                                'RESPONSÁVEL CLUBE',	'AGENTE',	'STATUS',	'CUSTO TOTAL'])
for row in rows:
    negoc.loc[len(negoc)] = row

st.write(negoc)


