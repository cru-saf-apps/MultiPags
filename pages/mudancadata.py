import streamlit as st
import pandas as pd
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
    
def parseStrToDt(s, format = '%m/%d/%Y'):
    return pd.NaT if s=='-' else datetime.strptime(s, format)
    
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']


credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = Client(scope = scope, creds = credentials)




spreadsheet_name = "BASE ELENCOS"
spread = Spread(spreadsheet_name, client = client)
sh = client.open(spreadsheet_name)
base_elencos = load_spreadsheet(spreadsheet_name)


parseStrToDt(base_elencos['Data Nascimento'],format = '%d/%m/%Y')


update_spreadsheet(spreadsheet_name,base_elencos)
