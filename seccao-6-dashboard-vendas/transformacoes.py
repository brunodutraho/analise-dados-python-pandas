import streamlit as st
import pandas as pd


@st.cache_data
def receita_por_estado(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Local da compra", as_index=False)["Preço"]
        .sum()
        .merge(
            df[["Local da compra", "lat", "lon"]].drop_duplicates(),
            on="Local da compra",
            how="left"
        )
        .sort_values("Preço", ascending=False)
    )


@st.cache_data
def receita_mensal(df: pd.DataFrame) -> pd.DataFrame:
    df_mensal = (
        df.set_index("Data da Compra")
        .groupby(pd.Grouper(freq="M"))["Preço"]
        .sum()
        .reset_index()
    )

    df_mensal["Ano"] = df_mensal["Data da Compra"].dt.year
    df_mensal["Mes"] = df_mensal["Data da Compra"].dt.month_name()
    df_mensal["Crescimento_%"] = df_mensal["Preço"].pct_change() * 100

    return df_mensal


@st.cache_data
def receita_por_categoria(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("Categoria do Produto", as_index=False)["Preço"]
        .sum()
        .sort_values("Preço", ascending=False)
    )


@st.cache_data
def performance_vendedores(df: pd.DataFrame) -> pd.DataFrame:
    df_perf = (
        df.groupby("Vendedor", as_index=False)
        .agg(
            Receita_Total=("Preço", "sum"),
            Quantidade_Vendas=("Preço", "count")
        )
    )

    df_perf["Ticket_Medio"] = (
        df_perf["Receita_Total"] /
        df_perf["Quantidade_Vendas"]
    )

    return df_perf


@st.cache_data
def pareto_vendedores(df_perf: pd.DataFrame) -> pd.DataFrame:
    df_pareto = df_perf.sort_values("Receita_Total", ascending=False).copy()

    df_pareto["%_Acumulado"] = (
        df_pareto["Receita_Total"].cumsum() /
        df_pareto["Receita_Total"].sum()
    ) * 100

    return df_pareto

@st.cache_data
def comparar_periodos(df, data_inicio, data_fim):
    """
    Compara o período selecionado com o período anterior equivalente.

    Retorna:
    - receita_atual
    - receita_anterior
    - variacao_percentual
    """

    periodo_atual = df[
        (df["Data da Compra"] >= data_inicio) &
        (df["Data da Compra"] <= data_fim)
    ]

    receita_atual = periodo_atual["Preço"].sum()

    # calcula duração do período
    dias_periodo = (data_fim - data_inicio).days

    # define período anterior equivalente
    data_fim_anterior = data_inicio - pd.Timedelta(days=1)
    data_inicio_anterior = data_fim_anterior - pd.Timedelta(days=dias_periodo)

    periodo_anterior = df[
        (df["Data da Compra"] >= data_inicio_anterior) &
        (df["Data da Compra"] <= data_fim_anterior)
    ]

    receita_anterior = periodo_anterior["Preço"].sum()

    if receita_anterior > 0:
        variacao_percentual = (
            (receita_atual - receita_anterior) / receita_anterior
        ) * 100
    else:
        variacao_percentual = 0

    return receita_atual, receita_anterior, variacao_percentual
