import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt





lista_anos = ['2020','2021']

lista_ligas = ['BRA1','BRA2','ARG1']

peso_ligas = {'BRA1':1, 'BRA2':0.5,'ARG1':0.9}

@st.cache
def gen_base(lista_anos, lista_ligas):
    base = pd.DataFrame()
    for liga in lista_ligas:
        for ano in lista_anos:
            for num in range(1,3):
                arquivo = liga+'-'+str(ano)+'-'+str(num)+'.csv'
                df = pd.read_csv(arquivo,sep=';',decimal=',')
                df['Ano'] = int(ano)
                df['Liga'] = liga
                base = pd.concat([base,df]).drop_duplicates().reset_index(drop=True)

    base = base.rename(columns={"Equipa dentro de um período de tempo seleccionado":"Equipe no ano",
                                "Equipa":"Equipe atual","Minutos jogados:":"Minutos"})
    
    base = base.dropna(subset=['Posição'])
    base = base.reset_index(drop=True)        

    cols_base = base.columns[-2:].tolist()
    for item in base.columns[:-2].tolist():
        cols_base.append(item)
    base = base[cols_base]
    
    return base

base = gen_base(lista_anos, lista_ligas)


st.subheader("Busca por Jogador")
pesq_rap = st.text_input('Digite o nome desejado:')

lista_results = []
nomes = pd.unique(base.Jogador).tolist()
t = 0
while t<len(nomes):
  if pesq_rap in nomes[t]:
    lista_results.append(nomes[t])
  t += 1

st.write(base[base.Jogador.isin(lista_results)][['Jogador','Equipe atual','Equipe no ano','Minutos jogados:','Ano','Liga']])
