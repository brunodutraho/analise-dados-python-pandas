import matplotlib.pyplot as plt

# 1-Dados Fictícios - Quantidade de Produtos Vendidos por Vendedores
vendedores = ['João', 'Maria', 'Pedro', 'Ana']
quantidade_vendida = [45, 60, 30, 55]

# 2-Criando o gráfico de barras
plt.figure(figsize=(8, 5))
barras = plt.bar(
    vendedores,
    quantidade_vendida,
    color='green'
)

# 3-Adicionando rótulos e título ao gráfico
plt.xlabel('Vendedores')
plt.ylabel('Quantidade Vendida')
plt.title('Quantidade de Produtos Vendidos por Vendedores')

plt.grid(axis='y', alpha=0.3)

# 4-Adicionando valores no topo das barras
for barra in barras:
    altura = barra.get_height()
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        altura,
        f'{altura}',
        ha='center',
        va='bottom'
    )

# 5-Exibir o gráfico
plt.tight_layout()
plt.show()
