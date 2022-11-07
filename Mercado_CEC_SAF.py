import streamlit as st
import base64


def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('cruzeiro-do-sul.jpg')  



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


