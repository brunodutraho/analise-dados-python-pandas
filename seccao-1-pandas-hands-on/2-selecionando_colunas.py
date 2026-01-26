from pathlib import Path

import streamlit as st
import pandas as pd

# ==================================================
# Configuração de caminhos
# ==================================================
# BASE_DIR garante que o caminho funcione corretamente
# independentemente de onde o script é executado
BASE_DIR = Path(__file__).parent
CAMINHO_ARQUIVO = BASE_DIR / "datasets" / "compras.csv"

# ==================================================
# Leitura dos dados
# ==================================================
# index_col=0 pois a coluna de data foi salva como índice
df_compras = pd.read_csv(
    CAMINHO_ARQUIVO,
    sep=";",
    decimal=",",
    index_col=0,
    parse_dates=True,
    encoding="utf-8"
)

# ==================================================
# Sidebar – Seleção de colunas
# ==================================================
st.sidebar.header("📊 Filtros de Visualização")

# Lista de colunas disponíveis
colunas = list(df_compras.columns)

# Permite selecionar quais colunas serão exibidas
colunas_selecionadas = st.sidebar.multiselect(
    "Selecione as colunas para exibição:",
    colunas,
    default=colunas  # exibe todas por padrão
)

# ==================================================
# Sidebar – Filtros dinâmicos
# ==================================================
# Divide a sidebar em duas colunas para organização visual
col1, col2 = st.sidebar.columns(2)

# Seleção da coluna de filtro
# Exclui id_compra por não fazer sentido filtrar por ID
col_filtro = col1.selectbox(
    "Filtrar por coluna:",
    [c for c in colunas if c != "id_compra"]
)

# Seleção do valor baseado na coluna escolhida
valor_filtro = col2.selectbox(
    "Valor:",
    sorted(df_compras[col_filtro].dropna().unique())
)

# Botões de ação
btn_filtrar = col1.button("🔎 Filtrar")
btn_limpar = col2.button("🧹 Limpar")

# ==================================================
# Lógica de exibição da tabela
# ==================================================
st.title("🛒 Base de Compras")

# Caso nenhum filtro seja aplicado, mostra apenas colunas selecionadas
df_exibicao = df_compras[colunas_selecionadas]

# Aplica o filtro somente quando o botão for acionado
if btn_filtrar:
    df_exibicao = df_exibicao.loc[
        df_compras[col_filtro] == valor_filtro
    ]

# Exibição final
st.dataframe(df_exibicao, use_container_width=True)
