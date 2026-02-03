import matplotlib.pyplot as plt

# 1-Dados ficticios - Venda ao longo dos meses
meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
vendas = [150, 200, 180, 300, 250, 400]

# 2-Criando o gráfico de linha
plt.figure(figsize=(8, 5))
plt.plot(
    meses,
    vendas,
    marker='o',
    linestyle='-',
    color='blue',
    label='Vendas Mensais'
)

# 3-Adicionando rótulos e título ao gráfico
plt.xlabel('Mês')
plt.ylabel('Quantidade de Vendas')
plt.title('Evolução das Vendas ao Longo dos Meses')

plt.legend()
plt.grid(alpha=0.3)

# 4-Exibindo o gráfico
plt.tight_layout()
plt.show()