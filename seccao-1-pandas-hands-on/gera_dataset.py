"""
Script de geração de dados fictícios
Seção 1 – Pandas Hands-on

Objetivo:
- Criar datasets simulados de compras, lojas e produtos
- Utilizado como base para aulas de Pandas e análises futuras

"""

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import names


# =====================================================
# Definição do diretório base e pasta de datasets
# =====================================================

BASE_DIR = Path(__file__).resolve().parent
PASTA_DATASETS = BASE_DIR / "datasets"

PASTA_DATASETS.mkdir(parents=True, exist_ok=True)


# =====================================================
# Dados base (dimensões)
# =====================================================

LOJAS = [
    {
        "estado": "SP",
        "cidade": "São Paulo",
        "vendedores": ["Ana Oliveira", "Lucas Pereira"],
    },
    {
        "estado": "MG",
        "cidade": "Belo Horizonte",
        "vendedores": ["Carlos Silva", "Fernanda Costa"],
    },
    {
        "estado": "RJ",
        "cidade": "Rio de Janeiro",
        "vendedores": ["Juliana Almeida", "Pedro Souza"],
    },
    {
        "estado": "RS",
        "cidade": "Porto Alegre",
        "vendedores": ["Mariana Gomes", "Roberto Ferreira"],
    },
    {
        "estado": "SC",
        "cidade": "Florianópolis",
        "vendedores": ["Gabriela Santos", "Lucas Pereira"],
    },
]

PRODUTOS = [
    {"id": 0, "nome": "Smartphone Samsung Galaxy", "preco": 2500},
    {"id": 1, "nome": "Notebook Dell Inspiron", "preco": 4500},
    {"id": 2, "nome": "Tablet Apple iPad", "preco": 3000},
    {"id": 3, "nome": "Smartwatch Garmin", "preco": 1200},
    {"id": 4, "nome": "Fone de Ouvido Sony", "preco": 600},
]

FORMAS_PAGAMENTO = ["cartão de crédito", "boleto", "pix", "dinheiro"]

GENEROS_CLIENTES = ["male", "female"]


# =====================================================
# Geração das compras (tabela fato)
# =====================================================

compras = []

for _ in range(2000):
    loja = random.choice(LOJAS)
    vendedor = random.choice(loja["vendedores"])
    produto = random.choice(PRODUTOS)

    data_compra = datetime.now() - timedelta(
        days=random.randint(1, 365),
        hours=random.randint(-5, 5),
        minutes=random.randint(-30, 30),
    )

    genero_cliente = random.choice(GENEROS_CLIENTES)
    nome_cliente = names.get_full_name(genero_cliente)

    compras.append(
        {
            "data": data_compra,
            "id_compra": 0,  # será preenchido após o DataFrame
            "loja": loja["cidade"],
            "vendedor": vendedor,
            "produto": produto["nome"],
            "cliente_nome": nome_cliente,
            "cliente_genero": genero_cliente.replace(
                "female", "feminino"
            ).replace("male", "masculino"),
            "forma_pagamento": random.choice(FORMAS_PAGAMENTO),
        }
    )


# =====================================================
# Criação dos DataFrames
# =====================================================

df_compras = (
    pd.DataFrame(compras)
    .set_index("data")
    .sort_index()
)

df_compras["id_compra"] = range(len(df_compras))

df_lojas = pd.DataFrame(LOJAS)
df_produtos = pd.DataFrame(PRODUTOS)


# =====================================================
# Exportação dos arquivos
# =====================================================

# CSV
df_compras.to_csv(PASTA_DATASETS / "compras.csv", sep=";", decimal=",")
df_lojas.to_csv(PASTA_DATASETS / "lojas.csv", sep=";", decimal=",")
df_produtos.to_csv(PASTA_DATASETS / "produtos.csv", sep=";", decimal=",")

# Excel
df_compras.to_excel(PASTA_DATASETS / "compras.xlsx")
df_lojas.to_excel(PASTA_DATASETS / "lojas.xlsx")
df_produtos.to_excel(PASTA_DATASETS / "produtos.xlsx")
