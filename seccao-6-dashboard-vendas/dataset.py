import json
import pandas as pd
import streamlit as st
from pathlib import Path
from core.validators import (
    validar_colunas_obrigatorias,
    tratar_valores_nulos
)

BASE_DIR = Path(__file__).parent
DATASET_PATH = BASE_DIR / 'datasets' / 'vendas.json'


@st.cache_data
def carregar_dados():
    with open(DATASET_PATH, encoding='utf-8') as file:
        data = json.load(file)

    df = pd.DataFrame(data)

    df['Data da Compra'] = pd.to_datetime(
        df['Data da Compra'],
        format='%d/%m/%Y'
    )

    validar_colunas_obrigatorias(df)
    df = tratar_valores_nulos(df)

    return df
