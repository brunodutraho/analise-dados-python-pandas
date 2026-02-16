import streamlit as st
from dataset import df
from utils import format_number, load_all_css
from transformacoes import (
    receita_por_estado,
    receita_mensal,
    receita_por_categoria,
    performance_vendedores,
    pareto_vendedores
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

# ================= CONFIGURAÇÃO =================
st.set_page_config(
    page_title="Dashboard de Vendas",
    layout="wide",
    page_icon="\U0001F4CA"
)

st.markdown(load_all_css(), unsafe_allow_html=True)

st.title("\U0001F4CA Dashboard Executivo de Vendas")
st.divider()

if df.empty:
    st.warning("\U000026A0 Dataset vazio.")
    st.stop()

# ================= FILTRO =================
st.sidebar.title('Filtro de Vendedores')
filtro_vendedor = st.sidebar.multiselect(
    'Vendedores',
    sorted(df['Vendedor'].dropna().unique())

)

df_filtrado = df.copy()
if filtro_vendedor:
    df_filtrado = df_filtrado[df_filtrado['Vendedor'].isin(filtro_vendedor)]

# ================= TRANSFORMAÇÕES =================
df_rec_estado = receita_por_estado(df)
df_rec_mensal = receita_mensal(df)
df_rec_categoria = receita_por_categoria(df)
df_perf = performance_vendedores(df)
df_pareto = pareto_vendedores(df_perf)

df_rec_vendedores = df_perf.sort_values("Receita_Total", ascending=False)
df_vendas_vendedores = df_perf.sort_values("Quantidade_Vendas", ascending=False)

# ================= KPIs =================
receita_total = df["Preço"].sum()
quantidade_vendas = df.shape[0]
ticket_medio = receita_total / quantidade_vendas
crescimento_mensal = df_rec_mensal["Crescimento_%"].iloc[-1]

estado_top = df_rec_estado.iloc[0]["Local da compra"]
valor_top = df_rec_estado.iloc[0]["Preço"]

# ===== METAS SIMULADAS =====
meta_receita = receita_total * 1.10
meta_vendas = quantidade_vendas * 1.05

delta_receita = receita_total - meta_receita
delta_vendas = quantidade_vendas - meta_vendas

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

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "\U0001F4B0 Receita Total",
        format_number(receita_total, prefix="R$ "),
        delta=format_number(delta_receita, prefix="R$ ")
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

    # ===== CONCENTRAÇÃO TOP 5 =====
    concentracao_top5 = (
        df_rec_estado.head(5)["Preço"].sum() / receita_total
    ) * 100

    st.caption(
        f"Os 5 principais estados representam "
        f"{concentracao_top5:.2f}% da receita total."
    )

    st.divider()

    col6, col7 = st.columns(2)

    with col6:
        st.subheader("\U0001F5FA Receita por Estado")
        st.plotly_chart(
            grafico_receita_estado_mapa(df_rec_estado),
            use_container_width=True,
            key="grafico_mapa_receita_estado"
        )

    with col7:
        st.subheader("\U0001F4C5 Receita Mensal")
        st.plotly_chart(
            grafico_receita_mensal(df_rec_mensal),
            use_container_width=True,
            key="grafico_receita_mensal"
        )

    col8, col9 = st.columns(2)

    with col8:
        st.subheader("\U0001F3C5 Top 5 Estados")
        st.plotly_chart(
            grafico_barra_receita_estado(df_rec_estado),
            use_container_width=True,
            key="grafico_top5_estados"
        )

    with col9:
        st.subheader("\U0001F4E6 Top 7 Categorias")
        st.plotly_chart(
            grafico_receita_categoria(df_rec_categoria),
            use_container_width=True,
            key="grafico_receita_categoria"
        )

    # ===== TABELAS =====
    st.divider()

    with st.expander("\U0001F4C4 Ver Tabela - Receita por Estado"):
        st.dataframe(df_rec_estado, use_container_width=True)

    with st.expander("\U0001F4C4 Ver Tabela - Receita por Categoria"):
        st.dataframe(df_rec_categoria, use_container_width=True)

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
        st.subheader("\U0001F4BC Receita por Vendedor")
        st.plotly_chart(
            grafico_receita_vendedores(df_rec_vendedores),
            use_container_width=True,
            key="grafico_receita_vendedores"
        )

    with col2:
        st.subheader("\U0001F4CA Vendas por Vendedor")
        st.plotly_chart(
            grafico_vendas_vendedores(df_vendas_vendedores),
            use_container_width=True,
            key="grafico_vendas_vendedores"
        )

    st.subheader("\U0001F4C9 Curva de Pareto")
    st.plotly_chart(
        grafico_pareto(df_pareto),
        use_container_width=True
    )

    st.divider()

    with st.expander("\U0001F4C4 Ver Tabela - Performance Completa Vendedores"):
        st.dataframe(
            df_perf.sort_values("Receita_Total", ascending=False),
            use_container_width=True,
            key="grafico_pareto"
        )

# ==========================================================
# ===================== ANÁLISES AVANÇADAS =================
# ==========================================================
with aba_analise:

    st.subheader("\U0001F4CA Distribuição de Preços")
    st.plotly_chart(
        grafico_histograma(df),
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
    st.dataframe(df, use_container_width=True)
