import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.set_page_config(layout='wide')

@st.cache_data
def gerar_df():
    df = pd.read_excel(
        io = "database.xlsx",
        engine = "openpyxl",
        sheet_name= "Pasta1",
        usecols= "A:Q",
        nrows= 22657
    )
    return df

df = gerar_df()

colunasUteis = ['MÊS', 'PRODUTO', 'REGIÃO', 'ESTADO', 'PREÇO MÉDIO REVENDA']

df = df[colunasUteis]

with st.sidebar:
    st.subheader('PL Data Analysis')
    logo = Image.open('LogoPL.png')
    st.image(logo, use_column_width=True)
    st.subheader('Seleção de Filtros')
    fProduto = st.selectbox(
        'Selecione o combustível',
        options= df['PRODUTO'].unique()
    )

    fEstado = st.selectbox(
        'Selecione o Estado',
        options= df['ESTADO'].unique()
    )

    dadosUsuario = df.loc[(
        df['PRODUTO'] == fProduto) &
        (df['ESTADO'] == fEstado)
    ]

updateDatas = dadosUsuario['MÊS'].dt.strftime('%Y/%b')

dadosUsuario['MÊS'] = updateDatas[0:]

st.header('Preços dos Combustíveis no Brasil: 2013 à 2024')
st.markdown('**Combustível selecionado :**  ' + fProduto)
st.markdown('**Estado selecionado :**  ' + fEstado)

grafCombEstado = alt.Chart(dadosUsuario).mark_line(
    point= alt.OverlayMarkDef(color='red', size=20)
).encode(
    x = 'MÊS:T',
    y = 'PREÇO MÉDIO REVENDA',
    strokeWidth = alt.value(3)
).properties(
    height = 700,
    width = 1000
)

st.altair_chart(grafCombEstado)
