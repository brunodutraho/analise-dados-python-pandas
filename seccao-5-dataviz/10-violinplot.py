import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Fixando seed para reprodutibilidade
np.random.seed(42)

# Violinplot para visualizar a distribuição de vendas por categoria
categorias = ['Eletrônicos', 'Roupas', 'Alimentos', 'Livros']

vendas = {
    'Categoria': np.random.choice(categorias, 1000),
    'Vendas': np.random.normal(loc=50, scale=20, size=1000).clip(0)
}

df = pd.DataFrame(vendas)

plt.figure(figsize=(8, 6))
sns.violinplot(
    x='Categoria',
    y='Vendas',
    data=df,
    palette='muted'
)
plt.title('Distribuição de Vendas por Categoria')
plt.xlabel('Categoria')
plt.ylabel('Vendas')
plt.tight_layout()
plt.show()
