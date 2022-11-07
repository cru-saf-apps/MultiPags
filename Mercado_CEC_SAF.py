import streamlit as st

st.title('Análise de Mercado / Scouting - Cruzeiro SAF')

st.subheader('Guia do site')

st.write('Opções disponíveis atualmente:')

st.markdown("- Rankeamento, por posição;")
st.markdown("- Comparação de jogadores, por variáveis específicas;")
st.markdown("- Encontrar jogadores similares, por variáveis específicas;")

st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    list-style-position: inside;
}
</style>
''', unsafe_allow_html=True)
