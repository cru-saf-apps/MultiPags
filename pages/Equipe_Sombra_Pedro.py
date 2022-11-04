import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import csv



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

@st.cache
def gen_df_jogs(base):
    df_jogs = base.drop_duplicates(subset = ['Jogador','Equipe atual'])
    
    return df_jogs

df_jogs = gen_df_jogs(base)

st.subheader('Busca Rápida')
pesq_rap = st.text_input('Digite o nome desejado:')

lista_results = []
nomes = pd.unique(base.Jogador).tolist()
t = 0
while t<len(nomes):
  if pesq_rap in nomes[t]:
    lista_results.append(nomes[t])
  t += 1

try:
    st.write(df_jogs[df_jogs.Jogador.isin(lista_results)].reset_index(drop=True)[['Jogador','Equipe atual','Idade']])
except:
    st.write('Digite o nome do jogador como consta no WyScout')


st.subheader('O que deseja fazer?')

opcao = st.radio('Selecione a opção desejada:',options = ['Ver shortlist / equipe sombra','Adicionar jogador','Remover jogador'])
lista = pd.read_csv('lista_pedro.csv')

if opcao == 'Adicionar jogador':
    
    st.write(lista)
    
    nome = st.text_input('Nome do jogador que deseja adicionar:')
    
    aux_df = df_jogs[df_jogs.Jogador == nome]
    
    if len(aux_df) > 1:
        st.write(aux_df[['Jogador','Equipe atual','Posição']])
        equipe = st.text_input('Equipe atual do jogador:')
        
        aux_df = df_jogs[(df_jogs.Jogador == nome)&(df_jogs['Equipe atual'] == equipe)]
        st.write(aux_df[['Jogador','Equipe atual','Posição']])
    
    else:
        st.write(aux_df[['Jogador','Equipe atual','Posição']])
    
    if len(aux_df) == 1:
        lista_add = []
        lista_add.append(aux_df.Jogador.tolist()[0])
        lista_add.append(aux_df['Equipe atual'].tolist()[0])
        lista_add.append(aux_df['Posição'].tolist()[0])

        with open('lista_pedro.csv','a') as f:
            writer = csv.writer(f)
            writer.writerow(lista_add)
            f.close()
    st.write(lista)
    
    
if opcao == 'Remover jogador':
    st.write(lista)
    
    nome = st.text_input('Qual jogador deseja remover?')
    
    aux_df = lista[lista.Jogador == nome]
    
    if len(aux_df) > 1:
        st.write(aux_df)
        equipe = st.text_input('Equipe atual do jogador:')
        
        aux_df = lista[(lista.Jogador == nome)&(lista['Equipe atual'] == equipe)]
        st.write(aux_df[['Jogador','Equipe atual','Posição']])
    
    else:
        st.write(aux_df[['Jogador','Equipe atual','Posição']])
    
    
    
    
