import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Fixando seed para reprodutibilidade
np.random.seed(42)

# 1-Dados fictícios de preços de ações por empresa e trimestre
empresas = ['Empresa A', 'Empresa B', 'Empresa C', 'Empresa D']
trimestre = ['T1', 'T2', 'T3', 'T4']

# valores aleatórios entre 0 a 100 para simular os preçoes das ações
dados = np.random.rand(4, 4) * 100

# 2-Criando um Dataframe com os dados
df = pd.DataFrame(
    dados,
    columns=trimestre,
    index=empresas
)

# 3-Heatmap para identificar padrões de variação de preços entre empresas e trimestres
plt.figure(figsize=(8, 6))
sns.heatmap(df, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Preço de Ações por Trimestre')
plt.xlabel('Trimestre')
plt.ylabel('Empresa')
plt.show()