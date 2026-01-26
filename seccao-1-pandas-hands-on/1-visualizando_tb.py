from pathlib import Path

import streamlit as st
import pandas as pd

# ==================================================
# Configuração de caminhos
# ==================================================
# Garante que o caminho funcione corretamente
# independente do local de execução (terminal, VS Code, Streamlit)
BASE_DIR = Path(__file__).parent
CAMINHO_COMPRAS = BASE_DIR / "datasets" / "compras.csv"

# ==================================================
# Leitura dos dados
# ==================================================
df_compras = pd.read_csv(
    CAMINHO_COMPRAS,
    sep=";",
    decimal=",",
    encoding="utf-8"
)

# ==================================================
# Interface
# ==================================================
st.title("📊 Base de Compras")

st.dataframe(
    df_compras,
    use_container_width=True
)
