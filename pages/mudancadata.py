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


base_elencos['Data Nascimento'] = pd.to_datetime(base_elencos['Data Nascimento'],errors='ignore',format='%d/%m/%Y',infer_date_time=True)


update_spreadsheet(spreadsheet_name,base_elencos)
