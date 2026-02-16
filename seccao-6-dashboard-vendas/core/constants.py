"""
constants.py
---------------------------------
Centraliza constantes e regras globais do projeto.
Evita valores mágicos espalhados no código.
"""

# ===============================
# COLUNAS OBRIGATÓRIAS
# ===============================

REQUIRED_COLUMNS = [
    "Preço",
    "Data da Compra",
    "Categoria do Produto",
    "Vendedor",
    "Local da compra",
]

# ===============================
# METAS PADRÃO
# ===============================

META_RECEITA_CRESCIMENTO = 0.10  # 10%
META_VENDAS_CRESCIMENTO = 0.05   # 5%

# ===============================
# REGRAS DE NEGÓCIO
# ===============================

LIMITE_CONCENTRACAO_REGIONAL = 0.40  # 40%
LIMITE_CONCENTRACAO_VENDEDOR = 0.35  # 35%

# ===============================
# MENSAGENS PADRÃO
# ===============================

MSG_DATASET_VAZIO = "⚠️ Dataset vazio."
MSG_SEM_DADOS_FILTRO = "⚠️ Sem dados para os filtros selecionados."
