import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# 1-Gerando dados aleatórios
x = np.random.rand(50)
y = np.random.rand(50)
z = np.random.rand(50)

# 2-Criando o gráfico de dispersão
plt.figure(figsize=(8, 6))
plt.scatter(x, y, alpha=0.7)
plt.title('Gráfico de Dispersão com Dados Aleatórios')
plt.xlabel('Eixo X')
plt.ylabel('Eixo Y')
plt.grid(alpha=0.3)

# 3-Exibir gráfico
plt.tight_layout()
plt.show()

# 4-Criando o gráfico 3d
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(x, y, z, alpha=0.8)

ax.set_xlabel('Eixo X')
ax.set_ylabel('Eixo Y')
ax.set_zlabel('Eixo Z')
ax.set_title('Gráfico de Dispersão em 3D')

plt.show()
