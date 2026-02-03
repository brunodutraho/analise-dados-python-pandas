import matplotlib.pyplot as plt
import numpy as np

# 1-Dados fictícios - Pontuações de um teste
pontuacoes = np.random.randint(50, 100, 100)

# 2-Criando o histograma
plt.figure(figsize=(8, 5))
plt.hist(
    pontuacoes,
    bins=10,
    color='skyblue',
    edgecolor='black'
)

# 3-Adicionando rótulo e título ao gráfico
plt.xlabel('Pontuação')
plt.ylabel('Frequência')
plt.title('Distribuição das Pontuações do Teste')
plt.grid(alpha=0.3)

# 4-Exibindo gráfico
plt.tight_layout()
plt.show()