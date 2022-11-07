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


vars_info = ['Ano','Liga','Jogador','Equipe atual','Equipe no ano','Posição','Idade','Valor de mercado',
             'Contrato termina','Naturalidade','País de nacionalidade','Pé','Altura','Peso','Emprestado','Partidas jogadas']


vars_abs = ['Minutos','Golos','Golos esperados','Assistências','Assistências esperadas','Cortes de carrinho ajust. à posse',
            'Cartões amarelos','Cartões vermelhos','Golos sem ser por penálti','Golos de cabeça','Remate',
            'Comprimento médio de passes, m','Comprimento médio de passes longos, m','Golos sofridos','Remates sofridos',
            'Jogos sem sofrer golos','Golos sofridos esperados','Golos expectáveis defendidos','Penaltis marcados']


ano_min = min(base.Ano)
ano_max = max(base.Ano)

peso_min = 0.25
peso_max = (1-peso_min)

posicoes = ['Goleiro', 'Lat. Direito', 'Lat. Esquerdo', 'Zagueiro', 'Médio Defensivo', 
            'Médio Box to Box', 'Médio Ofensivo', 'Meia', 'Extremo Direito',
            'Extremo Esquerdo', 'Centroavante', 'Segundo Atacante']


dic_posicoes = {'Goleiro':['GK'],
                'Lat. Direito':['RB'],
                'Lat. Esquerdo':['LB'],
                'Zagueiro': ['CB', 'RCB', 'LCB'],
               'Médio Defensivo':['RDMF', 'LDMF', 'DMF'],
                'Médio Box to Box':['LCMF', 'RCMF', 'CMF'],
               'Médio Ofensivo': ['LCMF', 'RCMF', 'CMF', 'AMF', 'RAMF', 'LAMF'],
                'Meia': ['AMF', 'RAMF', 'LAMF'],
               'Extremo Direito': ['RW', 'RAMF', 'RWF'],
               'Extremo Esquerdo': ['LW', 'LAMF', 'LWF'],
               'Centroavante': ['CF'],
               'Segundo Atacante': ['CF', 'AMF']}

    
lista_selec = []
for coluna in base.columns.tolist():
  if coluna not in vars_info:
    if coluna != 'Minutos':
      lista_selec.append(coluna)    



   
vars_select = st.multiselect("Selecione variáveis para encontrar jogadores similares",options=lista_selec)

vars_comp = ['Minutos']
vars_comp.extend(vars_select)

var = vars_info.copy()
var.extend(vars_comp)

@st.cache
def gen_base2(base):
    base2 = pd.DataFrame()

    for liga in pd.unique(base.Liga):
        base_liga = base[base.Liga == liga]
        for ano in pd.unique(base_liga.Ano):
            base_ano = base_liga[base_liga.Ano == ano]

            for coluna in base_ano.columns.tolist():
                if coluna not in vars_info:
                    base_ano[coluna] = (base_ano[coluna]-np.nanmin(base_ano[coluna]))/(np.nanmax(base_ano[coluna])-np.nanmin(base_ano[coluna]))
                else:
                    base_ano[coluna] = base_ano[coluna]

            base2 = pd.concat([base2,base_ano])
            
    return base2
        
        
base2 = gen_base2(base)


df_rank = base2[var].copy()

df_rank['Media'] = df_rank[vars_comp].mean(axis=1)
df_rank['SD'] = df_rank[vars_comp].std(axis=1)


@st.cache
def gen_df_jogs_pronto(df_rank, vars_comp):

    df_jogs = df_rank.copy().drop_duplicates(subset=['Jogador','Equipe atual']).drop(df_rank.columns[-(len(vars_select)+3):].tolist(),axis=1)

    dic_colunas = {}
    for coluna in df_rank.columns[-(len(vars_comp)+2):-2]:
        lista_medias = []

        for index, row in df_jogs.iterrows():
            if pd.isnull(df_jogs['Equipe atual'][index]):
                df_aux = df_rank[(df_rank.Jogador == df_jogs.Jogador[index])&(pd.isnull(df_rank['Equipe atual']) == True)]
            else:
                df_aux = df_rank[(df_rank.Jogador == df_jogs.Jogador[index])&(df_rank['Equipe atual'] == df_jogs['Equipe atual'][index])]
            lista_valores = []
            for liga in pd.unique(df_aux.Liga):
                for ano in pd.unique(df_aux[df_aux.Liga == liga]['Ano']):
                    aux_df = df_aux[(df_aux.Ano == ano)&(df_aux.Liga == liga)]
                    if ano == ano_min:
                        lista_valores.append(peso_ligas[liga]*peso_min*np.nanmean(aux_df[coluna]))
                    elif ano == ano_max:
                        lista_valores.append(peso_ligas[liga]*peso_max*np.nanmean(aux_df[coluna]))

            media = np.nanmean(lista_valores)
            lista_medias.append(media)

        dic_colunas[coluna] = lista_medias
        df_jogs[coluna] = dic_colunas[coluna]


    df_jogs['Media'] = df_jogs[vars_comp].mean(axis=1)
    df_jogs['SD'] = df_jogs[vars_comp].std(axis=1)                 

    df_jogs = df_jogs.dropna(subset=['Media'])
    df_jogs['Media'] = df_jogs['Media'].astype('float')
    
    return df_jogs


df_jogs = gen_df_jogs_pronto(df_rank,vars_comp)


nome_busca1 = st.text_input("Nome do primeiro jogador:")

if len(df_jogs[df_jogs.Jogador==nome_busca1]) == 0:
  st.write("Favor inserir o nome do jogador igual no WyScout")

elif len(pd.unique(df_jogs[df_jogs.Jogador==nome_busca1]['Equipe atual']))>1:
  st.write("Mais de um jogador disponível com este nome, favor inserir o clube atual do jogador desejado.")
  st.write(df_jogs[df_jogs.Jogador==nome_busca1][['Jogador','Equipe atual']])
  clube1 = st.text_input("Clube do primeiro jogador:")
  df1 = df_jogs[(df_jogs.Jogador==nome_busca1)&(df_jogs["Equipe atual"] == clube1)]
  st.write("Tabela resumo do jogador desejado:")
  st.write(df1[['Jogador','Equipe atual']])
    
else:
  df1 = df_jogs[df_jogs.Jogador == nome_busca1]
  st.write("Tabela resumo do jogador desejado:")
  st.write(df1[['Jogador','Equipe atual']])
  clube1 = df1['Equipe atual'].tolist()[0]


dic_jogador = {}

df_jogador = df_jogs[(df_jogs.Jogador == nome_busca1)&(df_jogs['Equipe atual'] == clube1)]
df_jogador = df_jogador.reset_index(drop=True)

for coluna in vars_select:
    dic_jogador[coluna] = df_jogador[coluna][0]


df_jogs_comp = pd.concat([df_jogador,df_jogs]).drop_duplicates(keep=False)

df_dif = df_jogs_comp.copy()

for coluna in vars_select:
    for index, row in df_jogs_comp.iterrows():
        ind_dif = abs((df_jogs_comp[coluna][index] - dic_jogador[coluna])/(np.nanmax(df_jogs_comp[coluna]) - np.nanmin(df_jogs_comp[coluna])))
        df_dif[coluna][index] = ind_dif
        
df_dif['Media'] = df_dif[vars_select].mean(axis=1)


@st.cache
def gen_df_show_pronto(df_dif, vars_select):
    df_show = df_dif[['Jogador','Posição','Equipe atual']]

    for coluna in df_dif.columns[-(len(vars_select)+3):-2]:
        df_show[coluna] = ""
        for index, row in df_show.iterrows():
            aux_df = base[(base.Jogador == df_show.Jogador[index])&(base['Equipe atual']==df_show['Equipe atual'][index])]
            if coluna in vars_abs:
                soma = np.nansum(aux_df[coluna])
            else:
                soma = np.nanmean(aux_df[coluna])

            df_show[coluna][index] = soma

    df_show['Media'] = df_dif['Media']
    
    df_show = df_show.rename(columns={'Media':'Diferença'})
    df_show = df_show.sort_values(by='Diferença',ascending = True)
    df_show = df_show.assign(Ranking = range(1,len(df_show)+1))

    return df_show

df_show = gen_df_show_pronto(df_jogs,vars_select)

st.write(df_show)
