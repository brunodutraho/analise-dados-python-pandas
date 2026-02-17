import streamlit as st
import pandas as pd
import numpy as np
from dataset import carregar_dados
from utils import format_currency_full, format_number, load_all_css, format_date_br
from transformacoes import (
    receita_por_estado,
    receita_mensal,
    receita_por_categoria,
    performance_vendedores,
    pareto_vendedores,
    comparar_periodos
)
from graficos import (
    grafico_receita_mensal,
    grafico_receita_estado_mapa,
    grafico_barra_receita_estado,
    grafico_receita_categoria,
    grafico_receita_vendedores,
    grafico_vendas_vendedores,
    grafico_pareto,
    grafico_histograma,
)
from core.filters import aplicar_filtros 
from auth import logout



# ================= CONFIGURAÇÃO =================
st.set_page_config(
    page_title="Dashboard de Vendas",
    layout="wide",
    page_icon="\U0001F4CA"
)
st.markdown(load_all_css(), unsafe_allow_html=True)

# ================= ESCONDER SIDEBAR SE NÃO AUTENTICADO =================
if not st.session_state.get("autenticado", False):
    st.markdown("""
        <style>
            [data-testid="stSidebar"] {
                display: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

# ================= AUTENTICAÇÃO =================

if "autenticado" not in st.session_state:
    st.session_state.autenticado = False
if "usuario" not in st.session_state:
    st.session_state.usuario = None

def tela_login():

    col1, col2, col3 = st.columns([1, 1.5, 1])

    with col2:

        st.markdown(
            "<div class='login-title'>Painel Análise de Vendas</div>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<div class='login-subtitle'>Acesse sua central de indicadores estratégicos</div>",
            unsafe_allow_html=True
        )

        USUARIOS = {
            "admin": "1234",
            "bruno": "abcd"
        }

        with st.form("form_login"):

            usuario = st.text_input(
                "Usuário",
                placeholder="Usuário",
                label_visibility="collapsed"
            )

            senha = st.text_input(
                "Senha",
                type="password",
                placeholder="Senha",
                label_visibility="collapsed"
            )

            submitted = st.form_submit_button("Entrar")

        if submitted:
            if usuario in USUARIOS and senha == USUARIOS[usuario]:
                st.session_state.autenticado = True
                st.session_state.usuario = usuario
                st.rerun()
            else:
                st.error("Usuário ou senha inválidos.")

        st.markdown("</div>", unsafe_allow_html=True)


# Se não estiver autenticado, mostra login e para execução
if not st.session_state.autenticado:
    tela_login()
    st.stop()
logout()

# ===============================
# CARREGAMENTO DE DADOS
# ===============================

df = carregar_dados()

st.markdown("<div class='main-title'>\U0001F4CA Dashboard Executivo de Vendas</div>", unsafe_allow_html=True)
st.markdown("<div class='section-divider'></div>", unsafe_allow_html=True)

if df.empty:
    st.warning("\U000026A0 Dataset vazio.")
    st.stop()

# ================= FILTROS =================

st.sidebar.title("Filtros Avançados")

filtro_vendedor = st.sidebar.multiselect(
    "Vendedores",
    sorted(df["Vendedor"].dropna().unique()),
    default=[]
)
formas_pagamento = st.sidebar.multiselect(
    "Forma de Pagamento",
    options=sorted(df["Tipo de pagamento"].unique())
)

data_min = df["Data da Compra"].min().date()
data_max = df["Data da Compra"].max().date()

periodo = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max)
)

if isinstance(periodo, tuple) and len(periodo) == 2:
    data_inicio = pd.to_datetime(periodo[0])
    data_fim = pd.to_datetime(periodo[1])
else:
    st.warning("Selecione um intervalo válido de datas.")
    st.stop()

tipo_comparacao = st.sidebar.radio(
    "Comparar com:",
    ["Período anterior", "Mesmo período do ano anterior"]
)


# ================= APLICAÇÃO DOS FILTROS =================

filtros = {
    "vendedores": filtro_vendedor,
    "formas_pagamento": formas_pagamento,
    "data_inicio": data_inicio,
    "data_fim": data_fim
}


df_filtrado = aplicar_filtros(df, filtros)

if df_filtrado.empty:
    st.warning("Sem dados para os filtros selecionados.")
    st.stop()
# ================= COMPARAÇÃO DE PERÍODO =================
receita_atual, receita_anterior, variacao_periodo = comparar_periodos(
    df,
    data_inicio,
    data_fim,
    tipo=tipo_comparacao
)

# ================= TRANSFORMAÇÕES =================
df_rec_estado = receita_por_estado(df_filtrado)
df_rec_mensal = receita_mensal(df_filtrado)
df_rec_categoria = receita_por_categoria(df_filtrado)
df_perf = performance_vendedores(df_filtrado)
df_pareto = pareto_vendedores(df_perf)

df_rec_vendedores = df_perf.sort_values("Receita_Total", ascending=False)
df_vendas_vendedores = df_perf.sort_values("Quantidade_Vendas", ascending=False)

# ================= KPIs =================
receita_total = df_filtrado["Preço"].sum()
quantidade_vendas = df_filtrado.shape[0]
ticket_medio = (
    receita_total / quantidade_vendas
    if quantidade_vendas > 0
    else 0
)
crescimento_mensal = (
    df_rec_mensal["Crescimento_%"]
    .replace([np.inf, -np.inf], 0)
    .fillna(0)
    .iloc[-1]
    if not df_rec_mensal.empty
    else 0
)

estado_top = (
    df_rec_estado.iloc[0]["Local da compra"]
    if not df_rec_estado.empty
    else "-"
)
valor_top = (
    df_rec_estado.iloc[0]["Preço"]
    if not df_rec_estado.empty
    else 0
)

# ===== METAS SIMULADAS =====
meta_receita = receita_total * 1.10
meta_vendas = quantidade_vendas * 1.05

delta_receita = receita_total - meta_receita
delta_vendas = quantidade_vendas - meta_vendas

# ================= TEXTO DINÂMICO KPI =================

if tipo_comparacao == "Período anterior":
    texto_comparacao = "vs período anterior"
else:
    texto_comparacao = "vs ano anterior"

if variacao_periodo > 0:
    indicador = "\U0001F53A"
elif variacao_periodo < 0:
    indicador = "\U0001F53B"
else:
    indicador = "\u2796"

# ================= ABAS =================
aba_receita, aba_vendedores, aba_analise, aba_dataset = st.tabs([
    "\U0001F4B0 Receita",
    "\U0001F464 Vendedores",
    "\U0001F4C8 Análises Avançadas",
    "\U0001F4C4 Dataset"
])

# ==========================================================
# ========================= RECEITA ========================
# ==========================================================
with aba_receita:

    st.markdown("<div class='kpi-container'>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns(5)


    col1.metric(
    "\U0001F4B0 Receita Total",
    format_number(receita_atual, prefix="R$ "),
    delta=f"{indicador} {variacao_periodo:.2f}% {texto_comparacao}"
    )

    col2.metric(
        "\U0001F4E6 Vendas",
        format_number(quantidade_vendas),
        delta=format_number(delta_vendas)
    )

    col3.metric(
        "\U0001F3AF Ticket Médio",
        format_number(ticket_medio, prefix="R$ ")
    )

    col4.metric(
        "\U0001F4C8 Crescimento Mensal",
        f"{crescimento_mensal:.2f}%",
        delta=f"{crescimento_mensal:.2f}%"
    )

    col5.metric(
        "\U0001F3C6 Estado Líder",
        estado_top
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ===== CONCENTRAÇÃO TOP 5 =====
    concentracao_top5 = (
        df_rec_estado.head(5)["Preço"].sum() / receita_total
    ) * 100

    st.caption(
        f"Os 5 principais estados representam "
        f"{concentracao_top5:.2f}% da receita total."
    )

    st.divider()

    st.markdown("<div class='chart-block'>", unsafe_allow_html=True)
    col6, col7 = st.columns(2)

    with col6:
        st.markdown("<div class='title-grafico'>\U0001F5FA Receita por Estado</div>", unsafe_allow_html=True)
        st.plotly_chart(
            grafico_receita_estado_mapa(df_rec_estado),
            use_container_width=True,
            key="grafico_mapa_receita_estado"
        )

    with col7:
        st.markdown("<div class='title-grafico'>\U0001F4C5 Receita Mensal</div>", unsafe_allow_html=True)
        st.plotly_chart(
            grafico_receita_mensal(df_rec_mensal),
            use_container_width=True,
            key="grafico_receita_mensal"
        )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='chart-block'>", unsafe_allow_html=True)
    col8, col9 = st.columns(2)

    with col8:
        st.markdown("<div class='title-grafico'>\U0001F3C5 Top 5 Estados</div>", unsafe_allow_html=True)
        st.plotly_chart(
            grafico_barra_receita_estado(df_rec_estado),
            use_container_width=True,
            key="grafico_top5_estados"
        )

    with col9:
        st.markdown("<div class='title-grafico'>\U0001F4E6 Top 7 Categorias</div>", unsafe_allow_html=True)
        st.plotly_chart(
            grafico_receita_categoria(df_rec_categoria),
            use_container_width=True,
            key="grafico_receita_categoria"
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # ===== TABELAS =====
    st.divider()

    with st.expander("\U0001F4C4 Ver Tabela - Receita por Estado"):
        st.dataframe(
            df_rec_estado.style.format({
                "Preço": format_currency_full
            }),
            use_container_width=True)

    with st.expander("\U0001F4C4 Ver Tabela - Receita por Categoria"):
        st.dataframe(
            df_rec_categoria.style.format({
                "Preço": format_currency_full
            }),
            use_container_width=True)

# ==========================================================
# ======================== VENDEDORES ======================
# ==========================================================
with aba_vendedores:

    vendedor_top = df_perf.sort_values(
        "Receita_Total", ascending=False
    ).iloc[0]["Vendedor"]

    receita_vendedor_top = df_perf.sort_values(
        "Receita_Total", ascending=False
    ).iloc[0]["Receita_Total"]

    participacao_vendedor_top = (
        receita_vendedor_top / receita_total
    ) * 100

    st.success(
        f"O vendedor {vendedor_top} é responsável por "
        f"{participacao_vendedor_top:.2f}% da receita total."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<div class='title-grafico'>\U0001F4BC Receita por Vendedor</div>", unsafe_allow_html=True)
        st.plotly_chart(
            grafico_receita_vendedores(df_rec_vendedores),
            use_container_width=True,
            key="grafico_receita_vendedores"
        )

    with col2:
        st.markdown("<div class='title-grafico'>\U0001F4CA Vendas por Vendedor</div>", unsafe_allow_html=True)
        st.plotly_chart(
            grafico_vendas_vendedores(df_vendas_vendedores),
            use_container_width=True,
            key="grafico_vendas_vendedores"
        )

    st.markdown("<div class='title-grafico'>\U0001F4C9 Curva de Pareto</div>", unsafe_allow_html=True)
    st.plotly_chart(
        grafico_pareto(df_pareto),
        use_container_width=True
    )

    st.divider()

    with st.expander("\U0001F4C4 Ver Tabela - Performance Completa Vendedores"):
        st.dataframe(
            df_perf
                .sort_values("Receita_Total", ascending=False)
                .style.format({
                    "Receita_Total": format_currency_full
                }),
            use_container_width=True,
            key="grafico_pareto"
        )

# ==========================================================
# ===================== ANÁLISES AVANÇADAS =================
# ==========================================================
with aba_analise:
    st.markdown("<div class='title-grafico'>\U0001F4CA Distribuição de Preços</div>", unsafe_allow_html=True)
    st.plotly_chart(
        grafico_histograma(df_filtrado),
        use_container_width=True
    )

    st.markdown("### \U0001F4A1 Análise Estratégica Automática")

    percentual_estado_top = (valor_top / receita_total) * 100

    if percentual_estado_top > 40:
        nivel_concentracao = "alta concentração"
    elif percentual_estado_top > 25:
        nivel_concentracao = "concentração moderada"
    else:
        nivel_concentracao = "distribuição equilibrada"

    st.info(
        f"{estado_top} lidera o faturamento com "
        f"{percentual_estado_top:.2f}% da receita total, "
        f"indicando {nivel_concentracao} regional. "
        "Recomenda-se avaliar estratégias de expansão ou diversificação."
    )

# ==========================================================
# ========================= DATASET ========================
# ==========================================================
with aba_dataset:

    st.subheader("\U0001F50D Visualização Completa do Dataset")
    st.dataframe(
        df_filtrado.style.format({
            "Preço": format_currency_full,
            "Data da Compra": format_date_br
        }), use_container_width=True)