import streamlit as st
import pandas as pd
import io
from dataset import carregar_dados
from auth import verificar_login, logout
from utils import format_currency_full, format_date_br
from utils import load_all_css

st.markdown(load_all_css(), unsafe_allow_html=True)
# ==========================================================
# CONDIÇÃO DE ACESSO
# ==========================================================
verificar_login()
logout()

# ==========================================================
# CACHE
# ==========================================================
@st.cache_data
def get_dataframe():
    return df.copy()

# ===============================
# CARREGAMENTO DE DADOS
# ===============================

df = carregar_dados()
# ==========================================================
# TÍTULO
# ==========================================================

st.markdown("<div class='main-title'>\U0001F4C4 Dataset de Vendas</div>", unsafe_allow_html=True)
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

df_base = get_dataframe()

# ==========================================================
# VALIDAÇÃO INICIAL
# ==========================================================
if df_base.empty:
    st.warning("\U000026A0 Dataset vazio.")
    st.stop()

# ==========================================================
# SELEÇÃO DE COLUNAS
# ==========================================================
with st.expander("\U0001F4CC Seleção de Colunas", expanded=False):
    colunas = st.multiselect(
        "Selecione as colunas desejadas:",
        options=df_base.columns.tolist(),
        default=df_base.columns.tolist()
    )

# ==========================================================
# SIDEBAR - FILTROS
# ==========================================================
st.sidebar.title("\U0001F50E Filtros")

# -------- Categoria --------
with st.sidebar.expander("\U0001F4E6 Categoria do Produto", expanded=True):
    categorias = st.multiselect(
        "Selecione as categorias:",
        options=sorted(df_base["Categoria do Produto"].unique()),
        default=sorted(df_base["Categoria do Produto"].unique())
    )

# -------- Preço --------
with st.sidebar.expander("\U0001F4B0 Faixa de Preço", expanded=True):
    preco_min = int(df_base["Preço"].min())
    preco_max = int(df_base["Preço"].max())

    faixa_preco = st.slider(
        "Selecione a faixa de preço:",
        min_value=preco_min,
        max_value=preco_max,
        value=(preco_min, preco_max)
    )

# -------- Data --------
with st.sidebar.expander("\U0001F4C5 Período da Compra", expanded=True):
    data_min = df_base["Data da Compra"].min().date()
    data_max = df_base["Data da Compra"].max().date()

    periodo = st.date_input(
        "Selecione o período:",
        value=(data_min, data_max)
    )

# ==========================================================
# APLICAÇÃO DOS FILTROS
# ==========================================================
df_filtrado = df_base.copy()

# Validação segura do intervalo
if isinstance(periodo, tuple) and len(periodo) == 2:
    data_inicio = pd.to_datetime(periodo[0])
    data_fim = pd.to_datetime(periodo[1])
else:
    st.warning("Selecione um intervalo válido de datas.")
    st.stop()

df_filtrado = df_filtrado[
    (df_filtrado["Categoria do Produto"].isin(categorias)) &
    (df_filtrado["Preço"].between(faixa_preco[0], faixa_preco[1])) &
    (df_filtrado["Data da Compra"].between(data_inicio, data_fim))
]

# ==========================================================
# RESULTADO
# ==========================================================
st.divider()
st.subheader("\U0001F4CA Resultado Filtrado")

st.caption(f"\U0001F522 {df_filtrado.shape[0]} registros encontrados.")

if df_filtrado.empty:
    st.warning("Nenhum registro encontrado com os filtros aplicados.")
    st.stop()

df_exibicao = df_filtrado[colunas]

st.dataframe(
    df_exibicao.style.format({
        "Preço": format_currency_full,
        "Frete": format_currency_full,
        "Data da Compra": format_date_br
    }),
    use_container_width=True,
    height=550
)

# ==========================================================
# DOWNLOADS
# ==========================================================
st.divider()
col1, col2 = st.columns(2)

# -------- CSV --------
with col1:
    csv = df_exibicao.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="\U0001F4C4 Baixar CSV",
        data=csv,
        file_name="dataset_filtrado.csv",
        mime="text/csv",
        use_container_width=True
    )

# -------- EXCEL --------
with col2:
    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_exibicao.to_excel(writer, index=False, sheet_name="Vendas")

    buffer.seek(0)
    
    st.download_button(
        label="\U0001F4CA Baixar Excel",
        data=buffer,
        file_name="dataset_filtrado.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

