# IMPORTAR BIBLIOTECAS
import streamlit as st  # Para criar a interface interativa
import pandas as pd     # Para manipulação de dados
import altair as alt    # Para criar gráficos interativos
from PIL import Image   # Para manipular e exibir imagens

# CONFIGURAÇÃO DA PÁGINA
# Define o layout da página como 'wide' (amplo) para otimizar o uso do espaço na tela
st.set_page_config(layout='wide')

# FUNÇÃO PARA GERAR O DATAFRAME
# A função 'gerar_df' carrega os dados de um arquivo Excel e retorna um dataframe pandas
# O decorador `@st.cache_data` garante que a função seja executada apenas uma vez e os dados sejam armazenados em cache para melhorar o desempenho
@st.cache_data
def gerar_df():
    df = pd.read_excel(
        io="database.xlsx",       # Caminho para o arquivo Excel
        engine="openpyxl",        # Motor necessário para ler o arquivo Excel
        sheet_name="Pasta1",      # Nome da aba que contém os dados
        usecols="A:Q",            # Colunas a serem carregadas
        nrows=22657               # Número de linhas a serem carregadas
    )
    return df

# CARREGANDO OS DADOS
df = gerar_df()

# FILTRANDO COLUNAS ÚTEIS
# Mantém apenas as colunas essenciais para a análise
colunasUteis = ['MÊS', 'PRODUTO', 'REGIÃO', 'ESTADO', 'PREÇO MÉDIO REVENDA']
df = df[colunasUteis]

# CONFIGURAR A BARRA LATERAL (SIDEBAR)
with st.sidebar:
    st.subheader('PL Data Analysis')  # Título da barra lateral
    # Exibe o logo da empresa
    logo = Image.open('LogoPL.png')  # Abre a imagem do logo
    st.image(logo, use_column_width=True)  # Exibe a imagem com o ajuste automático de largura
    
    st.subheader('Seleção de Filtros')  # Seção para seleção de filtros
    # Filtro de seleção do tipo de combustível
    fProduto = st.selectbox(
        'Selecione o combustível',  # Rótulo do selectbox
        options=df['PRODUTO'].unique()  # Opções são únicas da coluna 'PRODUTO'
    )
    
    # Filtro de seleção do estado
    fEstado = st.selectbox(
        'Selecione o Estado',  # Rótulo do selectbox
        options=df['ESTADO'].unique()  # Opções são únicas da coluna 'ESTADO'
    )
    
    # Filtra os dados de acordo com o combustível e o estado selecionados pelo usuário
    dadosUsuario = df.loc[(
        df['PRODUTO'] == fProduto) & 
        (df['ESTADO'] == fEstado)
    ]

# FORMATAÇÃO DA DATA
# Converte a coluna 'MÊS' para o formato ano/mês e altera a formatação do mês
updateDatas = dadosUsuario['MÊS'].dt.strftime('%Y/%b')
dadosUsuario['MÊS'] = updateDatas[0:]

# EXIBIÇÃO DOS DADOS NA PÁGINA PRINCIPAL
st.header('Preços dos Combustíveis no Brasil: 2013 à 2024')  # Cabeçalho principal da página
# Exibe o combustível selecionado pelo usuário
st.markdown('**Combustível selecionado :**  ' + fProduto)
# Exibe o estado selecionado pelo usuário
st.markdown('**Estado selecionado :**  ' + fEstado)

# CRIAÇÃO DO GRÁFICO INTERATIVO
# O gráfico de linhas mostra a evolução do preço médio de revenda por mês para o combustível e estado selecionados
grafCombEstado = alt.Chart(dadosUsuario).mark_line(
    # Adiciona pontos vermelhos nos dados do gráfico
    point=alt.OverlayMarkDef(color='red', size=20)
).encode(
    x='MÊS:T',  # Eixo X representa o mês
    y='PREÇO MÉDIO REVENDA',  # Eixo Y representa o preço médio de revenda
    strokeWidth=alt.value(3)  # Define a largura da linha do gráfico
).properties(
    height=700,  # Altura do gráfico
    width=1000   # Largura do gráfico
)

# EXIBIÇÃO DO GRÁFICO NA PÁGINA
st.altair_chart(grafCombEstado)  # Exibe o gráfico Altair na página