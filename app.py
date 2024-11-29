import pandas as pd
import streamlit as st
import plotly.express as px

# Função para carregar os dados com tratamento de encoding e separação correta de colunas
@st.cache_data
def carregar_dados():
    try:
        # Lê o CSV com o encoding correto e trata as aspas e os delimitadores
        dados = pd.read_csv(
            "dados/dados_consolidados.csv", 
            delimiter=",",  # Use vírgula como delimitador
            encoding="utf-8",  # Alterando para utf-8 para lidar com caracteres especiais
            quotechar='"',  # Tratando as aspas corretamente
            skipinitialspace=True  # Ignora espaços extras após delimitadores
        )
        return dados
    except pd.errors.ParserError as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()  # Retorna um DataFrame vazio em caso de erro

# Função para exibir o DataFrame de forma mais limpa
def exibir_dados(dados):
    if not dados.empty:
        st.dataframe(dados)  # Exibe os dados de forma interativa

# Carrega os dados
dados = carregar_dados()

# Sidebar para filtro de UF
st.sidebar.title("Filtro de Análise por UF")
uf_selecionada = st.sidebar.selectbox('Selecione o estado (UF)', dados['uf'].unique())

# Filtrando os dados com base na UF selecionada
dados_filtrados = dados[dados['uf'] == uf_selecionada]

# Exibe os dados filtrados
st.title(f"Análise de Acidentes de Trânsito - UF: {uf_selecionada}")
st.write(f"Analisando os dados de acidentes para o estado de {uf_selecionada}.")

# Exibe os dados filtrados
exibir_dados(dados_filtrados)

# 1. Distribuição de Acidentes por Dia da Semana
acidentes_por_dia = dados_filtrados['dia_semana'].value_counts().sort_index()

# Convertendo a série para um DataFrame para facilitar a criação do gráfico
acidentes_por_dia_df = acidentes_por_dia.reset_index()
acidentes_por_dia_df.columns = ['Dia da Semana', 'Número de Acidentes']  # Renomeia as colunas para um formato mais amigável

# Gráfico de barras com o número de acidentes por dia da semana
fig_dia_semana = px.bar(acidentes_por_dia_df, x='Dia da Semana', y='Número de Acidentes',
                        labels={'Dia da Semana': 'Dia da Semana', 'Número de Acidentes': 'Número de Acidentes'},
                        title="Distribuição de Acidentes por Dia da Semana")
st.plotly_chart(fig_dia_semana)

# 2. Distribuição de Acidentes por Tipo de Acidente
acidentes_por_tipo = dados_filtrados['tipo_acidente'].value_counts().sort_values(ascending=False)

# Convertendo a série para um DataFrame
acidentes_por_tipo_df = acidentes_por_tipo.reset_index()
acidentes_por_tipo_df.columns = ['Tipo de Acidente', 'Número de Acidentes']

# Gráfico de barras com o número de acidentes por tipo de acidente
fig_tipo_acidente = px.bar(acidentes_por_tipo_df, x='Tipo de Acidente', y='Número de Acidentes',
                           labels={'Tipo de Acidente': 'Tipo de Acidente', 'Número de Acidentes': 'Número de Acidentes'},
                           title="Distribuição de Acidentes por Tipo de Acidente")
st.plotly_chart(fig_tipo_acidente)

# 3. Distribuição de Acidentes por Causa de Acidente
acidentes_por_causa = dados_filtrados['causa_acidente'].value_counts().sort_values(ascending=False)

# Convertendo a série para um DataFrame
acidentes_por_causa_df = acidentes_por_causa.reset_index()
acidentes_por_causa_df.columns = ['Causa do Acidente', 'Número de Acidentes']

# Gráfico de barras com o número de acidentes por causa do acidente
fig_causa_acidente = px.bar(acidentes_por_causa_df, x='Causa do Acidente', y='Número de Acidentes',
                            labels={'Causa do Acidente': 'Causa do Acidente', 'Número de Acidentes': 'Número de Acidentes'},
                            title="Distribuição de Acidentes por Causa")
st.plotly_chart(fig_causa_acidente)

# 4. Acidentes por Condição Meteorológica
acidentes_por_condicao_meteorologica = dados_filtrados['condicao_metereologica'].value_counts().sort_values(ascending=False)

# Convertendo a série para um DataFrame
acidentes_por_condicao_df = acidentes_por_condicao_meteorologica.reset_index()
acidentes_por_condicao_df.columns = ['Condição Meteorológica', 'Número de Acidentes']

# Gráfico de barras com o número de acidentes por condição meteorológica
fig_condicao_meteorologica = px.bar(acidentes_por_condicao_df, x='Condição Meteorológica', y='Número de Acidentes',
                                    labels={'Condição Meteorológica': 'Condição Meteorológica', 'Número de Acidentes': 'Número de Acidentes'},
                                    title="Distribuição de Acidentes por Condição Meteorológica")
st.plotly_chart(fig_condicao_meteorologica)

# 5. Número total de mortos, feridos e ilesos
st.subheader("Totais de Mortes, Feridos e Ilesos")

if 'mortos' in dados.columns and 'feridos' in dados.columns and 'ilesos' in dados.columns:
    total_mortos = dados_filtrados['mortos'].sum()
    total_feridos = dados_filtrados['feridos'].sum()
    total_ilesos = dados_filtrados['ilesos'].sum()

    st.write(f"Mortos: {total_mortos}")
    st.write(f"Feridos: {total_feridos}")
    st.write(f"Ilesos: {total_ilesos}")
else:
    st.write("As colunas 'mortos', 'feridos' ou 'ilesos' não estão presentes nos dados.")
