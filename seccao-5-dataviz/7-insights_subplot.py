import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("datasets/Pedidos.csv")

# Criando uma única figura com quatro subplots
fig, ax = plt.subplots(2, 2, figsize=(15, 10))

# Gráfico 1 - Unidades vendidas por região
df.groupby('Regiao')['Unidades'].sum().plot(
    kind='bar',
    color='skyblue',
    ax=ax[0, 0]
)
ax[0, 0].set_title('Unidades Vendidas por Região')
ax[0, 0].set_xlabel('Região')
ax[0, 0].set_ylabel('Total de Unidades')
ax[0, 0].grid(alpha=0.3)
ax[0, 0].tick_params(axis='x', rotation=45)

# Gráfico 2 - Distribuição dos pedidos por item
df['Item'].value_counts().plot(
    kind='pie',
    autopct='%1.1f%%',
    startangle=90,
    ax=ax[0, 1]
)
ax[0, 1].set_title('Distribuição dos Pedidos por Item')
ax[0, 1].set_ylabel('')
ax[0, 1].axis('equal')

# Gráfico 3 - Relação preço x unidades
ax[1, 0].scatter(
    df['PrecoUnidade'],
    df['Unidades'],
    alpha=0.7,
    color='orange'
)
ax[1, 0].set_title('Preço Unitário vs Unidades')
ax[1, 0].set_xlabel('Preço Unitário')
ax[1, 0].set_ylabel('Unidades')
ax[1, 0].grid(alpha=0.3)

# Gráfico 4 - Evolução das vendas ao longo do tempo
df['DataPedido'] = pd.to_datetime(df['DataPedido'])
df['AnoMes'] = df['DataPedido'].dt.to_period('M').dt.to_timestamp()

df.groupby('AnoMes')['Unidades'].sum().plot(
    kind='line',
    marker='o',
    ax=ax[1, 1]
)
ax[1, 1].set_title('Unidades Vendidas ao Longo do Tempo')
ax[1, 1].set_xlabel('Período')
ax[1, 1].set_ylabel('Total de Unidades')
ax[1, 1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
