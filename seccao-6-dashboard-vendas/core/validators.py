"""
validators.py
---------------------------------
Módulo responsável por validações estruturais do dataset.
Garante integridade mínima antes de qualquer cálculo.
"""

from typing import List
import pandas as pd
import streamlit as st

from core.constants import REQUIRED_COLUMNS, MSG_DATASET_VAZIO


def validar_dataset_nao_vazio(df: pd.DataFrame) -> None:
    """
    Interrompe execução caso o dataset esteja vazio.
    """
    if df.empty:
        st.warning(MSG_DATASET_VAZIO)
        st.stop()


def validar_colunas_obrigatorias(
    df: pd.DataFrame,
    required_columns: List[str] = REQUIRED_COLUMNS
) -> None:
    """
    Verifica se todas as colunas obrigatórias existem no dataset.
    """
    colunas_ausentes = [
        col for col in required_columns if col not in df.columns
    ]

    if colunas_ausentes:
        st.error(
            f"\U0000274C Colunas obrigatórias ausentes: {colunas_ausentes}"
        )
        st.stop()


def tratar_valores_nulos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trata valores nulos críticos para evitar quebra de KPIs.
    Estratégia atual:
    - Preço: substituir por 0
    - Frete: substituir por 0
    """
    df = df.copy()

    if "Preço" in df.columns:
        df["Preço"] = df["Preço"].fillna(0)

    if "Frete" in df.columns:
        df["Frete"] = df["Frete"].fillna(0)

    return df
