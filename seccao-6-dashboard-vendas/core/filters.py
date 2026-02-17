"""
filters.py
---------------------------------
Centraliza aplicação de filtros no dataset.
Mantém regras de negócio fora da camada de interface.
"""

from typing import Dict, Any
import pandas as pd


def aplicar_filtros(df: pd.DataFrame, filtros: Dict[str, Any]) -> pd.DataFrame:
    """
    Aplica filtros combinados no DataFrame.

    Parâmetros:
    - df: DataFrame original
    - filtros: dicionário com regras de filtragem

    Retorna:
    - DataFrame filtrado
    """

    df_filtrado = df.copy()

    # Filtro por vendedores
    vendedores = filtros.get("vendedores")
    if vendedores:
        df_filtrado = df_filtrado[
            df_filtrado["Vendedor"].isin(vendedores)
        ]

    # Filtro por categorias
    categorias = filtros.get("categorias")
    if categorias:
        df_filtrado = df_filtrado[
            df_filtrado["Categoria do Produto"].isin(categorias)
        ]

    # Filtro por estados
    estados = filtros.get("estados")
    if estados:
        df_filtrado = df_filtrado[
            df_filtrado["Local da compra"].isin(estados)
        ]

    # Filtro por período
    data_inicio = filtros.get("data_inicio")
    data_fim = filtros.get("data_fim")

    if data_inicio and data_fim:
        df_filtrado = df_filtrado[
            df_filtrado["Data da Compra"].between(
                data_inicio,
                data_fim
            )
        ]
    
    # Filtro por forma de pagamento
    formas_pagamento = filtros.get("formas_pagamento")
    if formas_pagamento:
        df_filtrado = df_filtrado[
            df_filtrado["Tipo de pagamento"].isin(formas_pagamento)
        ]

    return df_filtrado
