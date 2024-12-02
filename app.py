import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
import random

@st.cache_data
def carregar_dados():
    try:
        dados = pd.read_csv(
            "dados/dados_final.csv",
            delimiter=",",
            encoding="utf-8",
            quotechar='"',
            skipinitialspace=True
        )
        return dados
    except pd.errors.ParserError as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return pd.DataFrame()

def gerar_paleta_cores(uf):
    # Define uma paleta de cores personalizada para cada UF
    random.seed(hash(uf))
    return random.choices(px.colors.qualitative.Dark24, k=7)

def analise_existente(dados_filtrados, cores):
    st.header("Análises Iniciais")
    
    # Distribuição por dia da semana
    acidentes_por_dia = dados_filtrados['dia_semana'].value_counts().sort_index()
    acidentes_por_dia_df = acidentes_por_dia.reset_index()
    acidentes_por_dia_df.columns = ['Dia da Semana', 'Número de Acidentes']
    
    fig_dia_semana = px.bar(acidentes_por_dia_df, x='Dia da Semana', y='Número de Acidentes',
                            title="Distribuição de Acidentes por Dia da Semana",
                            color_discrete_sequence=[cores[0]])
    st.plotly_chart(fig_dia_semana)
    
    # Distribuição por tipo de acidente
    acidentes_por_tipo = dados_filtrados['tipo_acidente'].value_counts().sort_values(ascending=False)
    acidentes_por_tipo_df = acidentes_por_tipo.reset_index()
    acidentes_por_tipo_df.columns = ['Tipo de Acidente', 'Número de Acidentes']
    
    fig_tipo_acidente = px.bar(acidentes_por_tipo_df, x='Tipo de Acidente', y='Número de Acidentes',
                               title="Distribuição por Tipo de Acidente",
                               color_discrete_sequence=[cores[1]])
    st.plotly_chart(fig_tipo_acidente)
    
    # Distribuição por causa
    acidentes_por_causa = dados_filtrados['causa_acidente'].value_counts().sort_values(ascending=False)
    acidentes_por_causa_df = acidentes_por_causa.reset_index()
    acidentes_por_causa_df.columns = ['Causa do Acidente', 'Número de Acidentes']
    
    fig_causa_acidente = px.bar(acidentes_por_causa_df, x='Causa do Acidente', y='Número de Acidentes',
                                title="Distribuição por Causa",
                                color_discrete_sequence=[cores[2]])
    st.plotly_chart(fig_causa_acidente)
    
    # Distribuição por condição meteorológica
    acidentes_por_condicao = dados_filtrados['condicao_metereologica'].value_counts()
    acidentes_por_condicao_df = acidentes_por_condicao.reset_index()
    acidentes_por_condicao_df.columns = ['Condição Meteorológica', 'Número de Acidentes']
    
    fig_condicao = px.bar(acidentes_por_condicao_df, x='Condição Meteorológica', y='Número de Acidentes',
                          title="Distribuição por Condição Meteorológica",
                          color_discrete_sequence=[cores[3]])
    st.plotly_chart(fig_condicao)

def analise_mitigacao(dados_filtrados, cores):
    st.header("Análise para Mitigação de Acidentes")
    
    # Análise por período do dia
    dados_filtrados['hora'] = dados_filtrados['horario'].str[:2].astype(int)
    dados_filtrados['periodo'] = pd.cut(dados_filtrados['hora'],
                                        bins=[0, 6, 12, 18, 24],
                                        labels=['Madrugada', 'Manhã', 'Tarde', 'Noite'])
    acidentes_periodo = pd.crosstab(dados_filtrados['periodo'], dados_filtrados['classificacao_acidente'])
    
    fig_periodo = px.bar(acidentes_periodo, title="Acidentes por Período e Gravidade",
                         labels={'value': 'Número de Acidentes', 'periodo': 'Período do Dia'},
                         color_discrete_sequence=[cores[4]])
    st.plotly_chart(fig_periodo)
    
    # Fatores de risco combinados
    st.subheader("Fatores de Risco Combinados")
    risco_combinado = dados_filtrados.groupby(['fase_dia', 'condicao_metereologica', 'tipo_pista']).agg({
        'id': 'count',
        'mortos': 'sum',
        'feridos': 'sum'
    }).reset_index()
    risco_combinado['indice_risco'] = (risco_combinado['mortos'] * 3 + risco_combinado['feridos']) / risco_combinado['id']
    top_riscos = risco_combinado.nlargest(10, 'indice_risco')
    
    st.write("Top 10 Combinações Mais Perigosas:")
    st.dataframe(top_riscos[['fase_dia', 'condicao_metereologica', 'tipo_pista', 'indice_risco']])
    
    # Mapa de calor temporal
    st.subheader("Distribuição Temporal dos Acidentes")
    dados_filtrados['mes'] = pd.to_datetime(dados_filtrados['data_inversa']).dt.month
    heatmap_data = dados_filtrados.pivot_table(
        values='id',
        index='hora',
        columns='mes',
        aggfunc='count',
        fill_value=0
    )
    fig_heatmap = px.imshow(heatmap_data, title="Mapa de Calor: Hora x Mês",
                            labels=dict(x="Mês", y="Hora do Dia", color="Número de Acidentes"),
                            color_continuous_scale=cores)
    st.plotly_chart(fig_heatmap)

def analise_avancada(dados_filtrados, cores):
    st.header("Análises Avançadas")
    
    # Distribuição de acidentes por BR
    acidentes_por_br = dados_filtrados['br'].value_counts().reset_index()
    acidentes_por_br.columns = ['BR', 'Número de Acidentes']
    fig_br = px.bar(acidentes_por_br, x='BR', y='Número de Acidentes',
                    title="Distribuição de Acidentes por BR",
                    color_discrete_sequence=[cores[5]])
    st.plotly_chart(fig_br)
    
    # Distribuição km por mortos, feridos leves, feridos graves, ilesos
    ferimentos_por_km = dados_filtrados.groupby('km').agg({
        'mortos': 'sum',
        'feridos_leves': 'sum',
        'feridos_graves': 'sum',
        'ilesos': 'sum'
    }).reset_index()
    fig_km = px.line(ferimentos_por_km, x='km', y=['mortos', 'feridos_leves', 'feridos_graves', 'ilesos'],
                     title="Distribuição de Ferimentos por KM",
                     labels={'value': 'Número de Pessoas', 'variable': 'Tipo de Ocorrência'},
                     color_discrete_sequence=cores)
    st.plotly_chart(fig_km)

def main():
    st.title("Dashboard Temporal de Acidentes de Trânsito no Brasil (2021-2024)")
    st.markdown("---")
    dados = carregar_dados()
    
    # Filtros
    st.sidebar.title("Filtros")
    uf_selecionada = st.sidebar.selectbox('Estado (UF)', dados['uf'].unique())
    
    # Aplicar filtros e definir cores
    cores = gerar_paleta_cores(uf_selecionada)
    dados_filtrados = dados[dados['uf'] == uf_selecionada]
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Acidentes", len(dados_filtrados))
    with col2:
        st.metric("Total de Mortos", dados_filtrados['mortos'].sum())
    with col3:
        st.metric("Total de Feridos Leves", dados_filtrados['feridos_leves'].sum())
    with col4:
        st.metric("Total de Feridos Graves", dados_filtrados['feridos_graves'].sum())
    
    # Chamadas das funções de análise
    analise_existente(dados_filtrados, cores)
    analise_mitigacao(dados_filtrados, cores)
    analise_avancada(dados_filtrados, cores)

if __name__ == "__main__":
    main()
