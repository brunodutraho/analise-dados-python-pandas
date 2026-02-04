import matplotlib.pyplot as plt
import numpy as np

# 1-Dados fictícios para os gráficos
x = np.arange(1, 6)
y1 = np.array([3, 5, 9, 7, 3])
y2 = np.array([1, 6, 2, 8, 4])

# 2-Criando subplots
fig, ax = plt.subplots(2, figsize=(8, 8))

# 3-Gráfico de barras no subplot superior
ax[0].bar(x, y1, color='skyblue')
ax[0].set_title('Distribuição de Valores - Barras')
ax[0].set_ylabel('Valores')
ax[0].grid(alpha=0.3)

# 4-Gráfico de linha no subplot inferior
ax[1].plot(x, y2, marker='o', linestyle='-', color='green')
ax[1].set_title('Evolução de Valores - Linha')
ax[1].set_xlabel('Eixo X')
ax[1].set_ylabel('Valores')
ax[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()