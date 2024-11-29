import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import calendar

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Acidentes de Trânsito no Brasil (2021-2024)",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Adicionando CSS personalizado para estilização
st.markdown(
    """
    <style>
    /* Fundo do Sidebar */
    .css-1d391kg {
        background-color: #f0f2f6;
    }
    /* Títulos */
    .css-1q1n0ol {
        color: #2e86de;
        font-size: 2rem;
        font-weight: bold;
    }
    /* Métricas */
    .metric {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    /* Cabeçalhos das análises */
    .css-1aumxhk {
        color: #2e86de;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Definindo uma paleta de cores para as UFs
uf_colors = {
    'AC': '#1f77b4', 'AL': '#ff7f0e', 'AP': '#2ca02c', 'AM': '#d62728',
    'BA': '#9467bd', 'CE': '#8c564b', 'DF': '#e377c2', 'ES': '#7f7f7f',
    'GO': '#bcbd22', 'MA': '#17becf', 'MT': '#aec7e8', 'MS': '#ffbb78',
    'MG': '#98df8a', 'PA': '#ff9896', 'PB': '#c5b0d5', 'PR': '#c49c94',
    'PE': '#f7b6d2', 'PI': '#c7c7c7', 'RJ': '#dbdb8d', 'RN': '#9edae5',
    'RS': '#f3b1a0', 'RO': '#b3e2cd', 'RR': '#fdc086', 'SC': '#d9d9d9',
    'SP': '#bc80bd', 'SE': '#ccebc5', 'TO': '#ffed6f'
}

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

def obter_cor_uf(uf_selecionada):
    return uf_colors.get(uf_selecionada, '#1f77b4')  # Padrão: azul

def analise_existente(dados_filtrados, cor):
    st.header("Análises Iniciais")
    
    # Distribuição por dia da semana
    acidentes_por_dia = dados_filtrados['dia_semana'].value_counts().sort_index()
    acidentes_por_dia_df = acidentes_por_dia.reset_index()
    acidentes_por_dia_df.columns = ['Dia da Semana', 'Número de Acidentes']
    
    fig_dia_semana = px.bar(
        acidentes_por_dia_df, 
        x='Dia da Semana', 
        y='Número de Acidentes',
        title="Distribuição de Acidentes por Dia da Semana",
        color_discrete_sequence=[cor]
    )
    fig_dia_semana.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_dia_semana, use_container_width=True)
    
    # Distribuição por tipo de acidente
    acidentes_por_tipo = dados_filtrados['tipo_acidente'].value_counts().sort_values(ascending=False)
    acidentes_por_tipo_df = acidentes_por_tipo.reset_index()
    acidentes_por_tipo_df.columns = ['Tipo de Acidente', 'Número de Acidentes']
    
    fig_tipo_acidente = px.bar(
        acidentes_por_tipo_df, 
        x='Tipo de Acidente', 
        y='Número de Acidentes',
        title="Distribuição por Tipo de Acidente",
        color_discrete_sequence=[cor]
    )
    fig_tipo_acidente.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_tipo_acidente, use_container_width=True)
    
    # Distribuição por causa
    acidentes_por_causa = dados_filtrados['causa_acidente'].value_counts().sort_values(ascending=False)
    acidentes_por_causa_df = acidentes_por_causa.reset_index()
    acidentes_por_causa_df.columns = ['Causa do Acidente', 'Número de Acidentes']
    
    fig_causa_acidente = px.bar(
        acidentes_por_causa_df, 
        x='Causa do Acidente', 
        y='Número de Acidentes',
        title="Distribuição por Causa",
        color_discrete_sequence=[cor]
    )
    fig_causa_acidente.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_causa_acidente, use_container_width=True)
    
    # Distribuição por condição meteorológica
    acidentes_por_condicao = dados_filtrados['condicao_metereologica'].value_counts()
    acidentes_por_condicao_df = acidentes_por_condicao.reset_index()
    acidentes_por_condicao_df.columns = ['Condição Meteorológica', 'Número de Acidentes']
    
    fig_condicao = px.bar(
        acidentes_por_condicao_df, 
        x='Condição Meteorológica', 
        y='Número de Acidentes',
        title="Distribuição por Condição Meteorológica",
        color_discrete_sequence=[cor]
    )
    fig_condicao.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_condicao, use_container_width=True)

def analise_mitigacao(dados_filtrados, cor):
    st.header("Análise para Mitigação de Acidentes")
    
    # Análise por período do dia
    dados_filtrados['hora'] = dados_filtrados['horario'].str[:2].astype(int)
    dados_filtrados['periodo'] = pd.cut(
        dados_filtrados['hora'],
        bins=[0,6,12,18,24],
        labels=['Madrugada','Manhã','Tarde','Noite'],
        right=False
    )
    
    acidentes_periodo = pd.crosstab(
        dados_filtrados['periodo'], 
        dados_filtrados['classificacao_acidente']
    )
    
    fig_periodo = px.bar(
        acidentes_periodo, 
        barmode='group',
        title="Acidentes por Período e Gravidade",
        labels={'value': 'Número de Acidentes', 'periodo': 'Período do Dia'},
        color_discrete_sequence=[cor, 'orange', 'red']
    )
    fig_periodo.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_periodo, use_container_width=True)
    
    # Fatores de risco combinados
    st.subheader("Fatores de Risco Combinados")
    risco_combinado = dados_filtrados.groupby(['fase_dia', 'condicao_metereologica', 'tipo_pista']).agg({
        'id': 'count',
        'mortos': 'sum',
        'feridos': 'sum'
    }).reset_index()
    
    risco_combinado['indice_risco'] = (risco_combinado['mortos']*3 + risco_combinado['feridos']) / risco_combinado['id']
    top_riscos = risco_combinado.nlargest(10, 'indice_risco')
    
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
    
    fig_heatmap = px.imshow(
        heatmap_data,
        title="Mapa de Calor: Hora x Mês",
        labels=dict(x="Mês", y="Hora do Dia", color="Número de Acidentes"),
        color_continuous_scale='Blues'
    )
    fig_heatmap.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_heatmap, use_container_width=True)

def analise_avancada(dados_filtrados, cor):
    st.header("Análises Avançadas")
    
    # Distribuição de acidentes por BR
    acidentes_por_br = dados_filtrados['br'].value_counts().reset_index()
    acidentes_por_br.columns = ['BR', 'Número de Acidentes']
    
    fig_br = px.bar(
        acidentes_por_br, 
        x='BR', 
        y='Número de Acidentes',
        title="Distribuição de Acidentes por BR",
        color_discrete_sequence=[cor]
    )
    fig_br.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_br, use_container_width=True)
    
    # Distribuição km por mortos, feridos leves, feridos graves, ilesos
    ferimentos_por_km = dados_filtrados.groupby('km').agg({
        'mortos': 'sum',
        'feridos_leves': 'sum',
        'feridos_graves': 'sum',
        'ilesos': 'sum'
    }).reset_index()
    
    fig_km = px.line(
        ferimentos_por_km, 
        x='km', 
        y=['mortos', 'feridos_leves', 'feridos_graves', 'ilesos'],
        title="Distribuição de Ferimentos por KM",
        labels={'value': 'Número de Pessoas', 'variable': 'Tipo de Ocorrência'},
        color_discrete_sequence=[cor, 'orange', 'red', 'green']
    )
    fig_km.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_km, use_container_width=True)
    
    # Distribuição delegacia por número de acidentes
    acidentes_por_delegacia = dados_filtrados['delegacia'].value_counts().reset_index()
    acidentes_por_delegacia.columns = ['Delegacia', 'Número de Acidentes']
    
    fig_delegacia = px.bar(
        acidentes_por_delegacia, 
        x='Delegacia', 
        y='Número de Acidentes',
        title="Distribuição de Acidentes por Delegacia",
        color_discrete_sequence=[cor]
    )
    fig_delegacia.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_delegacia, use_container_width=True)
    
    # Distribuição município por número de acidentes
    acidentes_por_municipio = dados_filtrados['municipio'].value_counts().reset_index()
    acidentes_por_municipio.columns = ['Município', 'Número de Acidentes']
    
    fig_municipio = px.bar(
        acidentes_por_municipio, 
        x='Município', 
        y='Número de Acidentes',
        title="Distribuição de Acidentes por Município",
        color_discrete_sequence=[cor]
    )
    fig_municipio.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_municipio, use_container_width=True)
    
    # Distribuição veículos por número de acidentes
    acidentes_por_veiculos = dados_filtrados.groupby('veiculos').size().reset_index(name='Número de Acidentes')
    fig_veiculos = px.scatter(
        acidentes_por_veiculos, 
        x='veiculos', 
        y='Número de Acidentes',
        title="Distribuição de Veículos por Número de Acidentes",
        color_discrete_sequence=[cor],
        size='Número de Acidentes',
        hover_name='veiculos',
        labels={'veiculos': 'Veículos', 'Número de Acidentes': 'Número de Acidentes'}
    )
    fig_veiculos.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_veiculos, use_container_width=True)

def main():
    st.title("🚦 Dashboard Temporal de Acidentes de Trânsito no Brasil (2021-2024) 🚦")

    st.markdown("---")

    dados = carregar_dados()
    
    if dados.empty:
        st.warning("Nenhum dado para exibir...")
        return
    
    # Filtros
    st.sidebar.title("Filtros")
    uf_selecionada = st.sidebar.selectbox('Estado (UF)', sorted(dados['uf'].unique()))
    cor_uf = obter_cor_uf(uf_selecionada)
    
    # Aplicar filtros
    dados_filtrados = dados[dados['uf'] == uf_selecionada]
    
    # Métricas principais
    st.markdown("### 📊 Métricas Principais")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Acidentes", len(dados_filtrados))
    with col2:
        st.metric("Total de Mortos", dados_filtrados['mortos'].sum())
    with col3:
        st.metric("Total de Feridos Leves", dados_filtrados['feridos_leves'].sum())
    with col4:
        st.metric("Total de Feridos Graves", dados_filtrados['feridos_graves'].sum())
    
    st.markdown("---")
    
    # Chamar análises
    analise_existente(dados_filtrados, cor_uf)
    analise_mitigacao(dados_filtrados, cor_uf)
    analise_avancada(dados_filtrados, cor_uf)
    
    # Rodapé
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Desenvolvido por [Manuel Lucala Zengo e Manuel Finda Evaristo]. Dados de 2021 a 2024."
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
