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
