"""
Dashboard de Vendas — Streamlit
================================

Como rodar localmente:
    pip install -r requirements.txt
    streamlit run meu_dashboard.py

Espera um arquivo 'vendas.csv' na mesma pasta, com as colunas:
    pedido_id, data, categoria, produto, quantidade, preco_unitario, receita
"""

import streamlit as st
import pandas as pd


# ---------------------------------------------------------------------------
# FASE 1 — Estrutura básica e otimização de desempenho
# ---------------------------------------------------------------------------

st.set_page_config(page_title="Dashboard de Vendas", layout="wide")
st.title("Dashboard de Vendas")


@st.cache_data
def carregar_dados(caminho_csv: str) -> pd.DataFrame:
    """Lê o CSV de vendas e faz o parsing da coluna de data.

    O decorador @st.cache_data guarda o resultado em memória: enquanto o
    argumento 'caminho_csv' não mudar, o Streamlit reaproveita o DataFrame
    já carregado em vez de ler o arquivo de novo a cada interação do
    usuário (cada clique em um filtro reexecuta o script inteiro).
    """
    df = pd.read_csv(caminho_csv, parse_dates=["data"])
    return df


df = carregar_dados("vendas.csv")


# ---------------------------------------------------------------------------
# FASE 2 — Layout e filtros laterais (interatividade)
# ---------------------------------------------------------------------------

st.sidebar.title("Filtros")

lista_categorias = sorted(df["categoria"].unique())
categorias_selecionadas = st.sidebar.multiselect(
    "Selecione as Categorias",
    options=lista_categorias,
    default=lista_categorias,  # começa com tudo selecionado
)

data_min = df["data"].min().date()
data_max = df["data"].max().date()
periodo_selecionado = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max,
)

# Regra de ouro do Streamlit: o valor retornado pelo widget filtra o
# DataFrame. Toda vez que o usuário muda o filtro, o script roda de novo
# do início e o df_filtrado é recalculado com o novo recorte.
df_filtrado = df[df["categoria"].isin(categorias_selecionadas)]

if isinstance(periodo_selecionado, tuple) and len(periodo_selecionado) == 2:
    inicio, fim = periodo_selecionado
    df_filtrado = df_filtrado[
        (df_filtrado["data"].dt.date >= inicio) & (df_filtrado["data"].dt.date <= fim)
    ]

if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
    st.stop()


# ---------------------------------------------------------------------------
# FASE 3 — Métricas em destaque e visualização de dados
# ---------------------------------------------------------------------------

# Passo 1: colunas proporcionais para os indicadores.
col1, col2 = st.columns([1, 1])

receita_calculada = df_filtrado["receita"].sum()
total_pedidos = df_filtrado["pedido_id"].nunique()

# Passo 2: indicadores numéricos em destaque.
# Atenção: o parâmetro correto de st.metric() é "value" (não "valor").
with col1:
    st.metric(label="Receita Total", value=f"R$ {receita_calculada:,.2f}")

with col2:
    st.metric(label="Total de Pedidos", value=f"{total_pedidos}")

# Passo 3: navegação por abas.
aba1, aba2 = st.tabs(["Evolução Mensal", "Tabela de Dados"])

# Passo 4: receita agrupada por mês, plotada em gráfico de área.
with aba1:
    st.subheader("Receita por mês")

    dados_mensais = (
        df_filtrado
        .assign(mes=df_filtrado["data"].dt.to_period("M").dt.to_timestamp())
        .groupby("mes", as_index=True)["receita"]
        .sum()
        .sort_index()
    )
    # dados_mensais tem o mês como índice e a receita como valor, no
    # formato que st.area_chart espera para plotar uma única série.
    st.area_chart(dados_mensais)

# Passo 5: tabela interativa + botão de download do recorte filtrado.
with aba2:
    st.subheader("Dados filtrados")

    st.dataframe(df_filtrado, use_container_width=True)

    csv_bytes = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar dados filtrados (CSV)",
        data=csv_bytes,
        file_name="vendas_filtrado.csv",
        mime="text/csv",
    )
