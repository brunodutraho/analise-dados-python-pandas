import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("datasets/Pedidos.csv")

# Gráfico 1-Quantidade de Unidades vendidas por região
ax = df.groupby('Regiao')['Unidades'].sum().plot(
    kind='bar',
    figsize=(8, 6),
    color='skyblue'
)
ax.set_title('Quantidade de Unidades Vendidas por Região')
ax.set_xlabel('Região')
ax.set_ylabel('Total de Unidades Vendidas')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Gráfico 2-Distribuição das vendas por item
plt.figure(figsize=(8, 6))
df['Item'].value_counts().plot(
    kind='pie',
    autopct='%1.2f%%',
    startangle=90
)
plt.title('Distribuição dos Pedidos por Item')
plt.axis('equal')
plt.tight_layout()
plt.show()

# Gráfico 3-Relação entre preço unitário e quantidade de unidades
plt.figure(figsize=(8, 6))
plt.scatter(
    df['PrecoUnidade'],
    df['Unidades'],
    color='orange',
    alpha=0.7
)
plt.title('Relação entre Preço Unitário e Quantidade de Unidades')
plt.xlabel('Preço Unitário')
plt.ylabel('Quantidade de Unidades')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Gráfico 4-Quantidade de Unidades Vendidas ao Longo do Tempo
# Convertendo a coluna DataPedido para o formato de data
df['DataPedido'] = pd.to_datetime(df['DataPedido'])

serie = df.groupby(df['DataPedido'].dt.to_period('M'))['Unidades'].sum()
serie.index = serie.index.astype(str)

serie.plot(
    kind='line',
    marker='o',
    color='green',
    figsize=(10, 6)
)
plt.title('Quantidade de Unidades Vendidas ao Longo do Tempo')
plt.xlabel('Data do Pedido')
plt.ylabel('Total de Unidades Vendidas')
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

# Gráfico 5-Quantidade de Unidades Vendidas por Estado em cada região
pivot = df.pivot_table(
    index='Estado',
    columns='Regiao',
    values='Unidades',
    aggfunc='sum',
    fill_value=0,
    
)
ax = pivot.plot(
    kind='bar',
    stacked=True,
    figsize=(10, 6)
)
ax.set_title('Quantidade de Unidades Vendidas por Estado em cada Região')
ax.set_xlabel('Estado')
ax.set_ylabel('Total de Unidades Vendidas')
ax.legend(
    title='Regiao',
    loc='upper left',
    bbox_to_anchor=(1.05, 1)
)
ax.grid(alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
