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

df_clubes = pd.DataFrame()

for liga in lista_ligas:
    for ano in lista_anos:
        aux_df = base[(base.Ano == int(ano)) & (base.Liga == liga)]
        
        clubes = pd.unique(aux_df['Equipe no ano'])
        
        df = pd.DataFrame({'Clube':clubes,'Liga':liga,'Ano':int(ano)})
        
        df_clubes = pd.concat([df_clubes,df])
                
df_clubes = df_clubes.dropna()
df_clubes = df_clubes.reset_index(drop=True)


vars_info = ['Ano','Liga','Jogador','Equipe atual','Equipe no ano','Posição','Idade','Valor de mercado',
             'Contrato termina','Naturalidade','País de nacionalidade','Pé','Altura','Peso','Emprestado','Partidas jogadas']


vars_abs = ['Minutos','Golos','Golos esperados','Assistências','Assistências esperadas','Cortes de carrinho ajust. à posse',
            'Cartões amarelos','Cartões vermelhos','Golos sem ser por penálti','Golos de cabeça','Remate',
            'Comprimento médio de passes, m','Comprimento médio de passes longos, m','Golos sofridos','Remates sofridos',
            'Jogos sem sofrer golos','Golos sofridos esperados','Golos expectáveis defendidos','Penaltis marcados']

@st.cache
def gen_df_clubes(base,df_clubes,vars_abs,vars_info):
  for coluna in base.columns:
      if coluna not in vars_info:
          df_clubes[coluna] = ''
          for index, row in df_clubes.iterrows():
              if coluna in vars_abs:
                  valor_time = np.nansum( base[(base.Ano == df_clubes.Ano[index]) & (base.Liga == df_clubes.Liga[index]) & (base['Equipe no ano'] == df_clubes.Clube[index])][coluna])
              else:
                  valor_time = np.nanmean( base[(base.Ano == df_clubes.Ano[index]) & (base.Liga == df_clubes.Liga[index]) & (base['Equipe no ano'] == df_clubes.Clube[index])][coluna])
              df_clubes[coluna][index] = valor_time
              
  return df_clubes

df_clubes = gen_df_clubes(base,df_clubes,vars_abs,vars_info)      



vars_select = st.multiselect('Selecione as variáveis para comparação de equipes:',options = df_clubes.columns.tolist())


equipe = st.selectbox('Selecione a equipe base:', options = pd.unique(df_clubes.Clube))

ano = st.selectbox('Selecione o ano da equipe selecionada para comparação:', options = pd.unique(df_clubes[df_clubes.Clube == equipe]['Ano']))

dic_equipe = {}

df_equipe = df_clubes[(df_clubes.Clube == equipe)&(df_clubes.Ano == ano)].reset_index(drop=True)

df_equipes_comp = pd.concat([df_equipe,df_clubes]).drop_duplicates(keep=False)

for coluna in vars_select:
    dic_equipe[coluna] = df_equipe[coluna][0]
    
df_dif = df_equipes_comp[vars_select].copy()
df_dif['Clube'] = df_equipes_comp.Clube
df_dif['Liga'] = df_equipes_comp.Liga
df_dif['Ano'] = df_equipes_comp.Ano

for coluna in vars_select:
    for index, row in df_equipes_comp.iterrows():
        ind_dif = abs((df_equipes_comp[coluna][index] - dic_equipe[coluna])/(np.nanmax(df_clubes[coluna]) - np.nanmin(df_clubes[coluna])))
        df_dif[coluna][index] = ind_dif
        
df_dif['Media'] = df_dif[vars_select].mean(axis=1)

st.write(df_dif)
