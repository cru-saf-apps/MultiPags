import streamlit as st
import pandas as pd
import openpyxl
from fpdf import FPDF
import base64


def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'


negoc = pd.read_excel('NEGOCIAÇÕES.xlsx',engine='openpyxl')
hist = pd.read_excel('HISTÓRICO.xlsx',engine='openpyxl')
hist['DATA HISTÓRICO'] = pd.to_datetime(hist['DATA HISTÓRICO']).dt.date


df_hist = pd.DataFrame()

for jogador in negoc.ID:
  
  hist_jog = hist[hist['ID ATLETA'] == jogador].reset_index(drop=True)
  comp = len(hist_jog)
  
  st.title(hist_jog[hist_jog['ID ATLETA']==jogador]['ATLETA'].tolist()[0])
  
  t = 1
  while t <= comp:
    
    st.subheader(hist_jog['DATA HISTÓRICO'][t-1])
    st.write(hist_jog['DESCRIÇÃO HISTÓRICO'][t-1])

    t+=1

export_as_pdf = st.button("Export Report")

if export_as_pdf:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(40, 10, report_text)
    
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), "test")

    st.markdown(html, unsafe_allow_html=True)
