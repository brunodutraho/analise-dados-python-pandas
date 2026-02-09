import seaborn as sns
import plotly.express as px

# Carregando dataset Diamonds (Seaborn)
data = sns.load_dataset('diamonds')

# Amostra para melhor performance na visualização interativa
data = data.sample(3000, random_state=42)

# Gráfico de dispersão interativo
fig = px.scatter(
    data,
    x='carat',
    y='price',
    color='cut',
    size='depth',
    hover_data=['x', 'y'],
    title='Dispersão de Diamantes: Peso vs Preço',
    template='plotly_white'
)

fig.show()
