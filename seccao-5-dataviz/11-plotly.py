import plotly.graph_objs as go
import pandas as pd
import numpy as np

# Dados fictícios de preços ao longo do tempo
dates = pd.date_range(start='2023-01-01', periods=100)

df = pd.DataFrame({
    'Date': dates,
    'Stock A': 100 + np.arange(100),
    'Stock B': 120 - np.arange(100),
    'Stock C': 90 + np.arange(100) * 0.5
})

# Gráfico de linhas interativo
fig = go.Figure()

for col in ['Stock A', 'Stock B', 'Stock C']:
    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df[col],
        mode='lines',
        name=col
    ))

fig.update_layout(
    title='Variação de Preço ao Longo do Tempo',
    xaxis_title='Data',
    yaxis_title='Preço',
    hovermode='x unified',
    template='plotly_white',
    legend=dict(orientation='h', y=-0.2)
)

fig.show()
