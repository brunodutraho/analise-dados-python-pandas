import plotly.express as px

# Mapa contendo a receita por estados
def grafico_receita_estado(df_rec_estado):

    df_plot = df_rec_estado.copy()

    df_plot['Receita Formatada'] = df_plot['Preço'].apply(
        lambda x: f'R$ {x:,.2f}'
    )
    
    fig = px.scatter_mapbox(
        df_plot,
        lat='lat',
        lon='lon',
        size='Preço',
        color='Preço',
        hover_name='Local da compra',
        custom_data=['Receita Formatada'],
        zoom=3.2,
        height=520,
        size_max=60,
        mapbox_style='carto-positron',
        color_continuous_scale='Viridis'
    )

    fig.update_traces(
            hovertemplate=
            "<b>%{hovertext}</b><br>" +
            "Receita: %{customdata[0]}<extra></extra>"
        )

    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
    )

    return fig

# Gráfico de Barras da receita por estados
def grafico_barra_receita_estado(df_rec_estado):

    df_plot = (
            df_rec_estado
            .sort_values('Preço', ascending=False)
            .head(5)
            .copy()
        )

    df_plot['Receita Formatada'] = df_plot['Preço'].apply(
        lambda x: f'R$ {x:,.2f}'
    )

    fig = px.bar(
        df_plot,
        x= 'Local da compra',
        y= 'Preço',
        height=520,
        text= 'Receita Formatada',
    )

    fig.update_traces(
        marker_color='#1F4E79',
        textposition='outside',
        customdata=df_plot[["Receita Formatada"]],
        hovertemplate=
        "<b>%{x}</b><br><br>" +
        "Receita: %{customdata[0]}" +
        "<extra></extra>"
    )

    fig.update_layout(
        yaxis=dict(range=[0, df_plot['Preço'].max()]),
        yaxis_title='Receita',
        xaxis_title='Estado',
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False,
        uniformtext_minsize=10,
        uniformtext_mode='hide'
        )

    return fig

# Gráfico de linhas da receita mensal
def grafico_receita_mensal(df_rec_mensal):
    
    df_plot = df_rec_mensal.copy()

    df_plot['Receita Formatada'] = df_plot['Preço'].apply(
        lambda x: f'R$ {x:,.2f}'
    )
    fig = px.line(
        df_plot,
        x = 'Data da Compra',
        y = 'Preço',
        markers = True,
        color = 'Ano',
        height=520,
        custom_data=['Receita Formatada'],
        range_y=[0, df_plot['Preço'].max()]
    )
    
    fig.update_traces(
        hovertemplate=
        "<b>%{x}</b><br>" +
        "Receita: %{customdata[0]}<extra></extra>"
    )

    fig.update_layout(
        yaxis=dict(range=[0, df_plot['Preço'].max()]),
        yaxis_title = 'Receita',
        margin=dict(l=0, r=0, t=40, b=0)
    )


    return fig

# Gráfico de barras receita por categoria
def grafico_receita_categoria(df_rec_categoria):
    
    df_plot = (
        df_rec_categoria
        .head(7)
        .copy()
    )

    df_plot['Receita Formatada'] = df_plot['Preço'].apply(
        lambda x: f'R$ {x:,.2f}'
    )

    fig = px.bar(
        df_plot,
        x = 'Categoria do Produto',
        y = 'Preço',
        height = 520,
        text = 'Receita Formatada',
    )

    fig.update_traces(
        marker_color='#1F4E79',
        textposition='outside',
        customdata=df_plot[['Receita Formatada']],
        hovertemplate=
        "<b>%{x}</b><br><br>" +
        "Receita: %{customdata[0]}" +
        "<extra></extra>"
    )

    
    fig.update_layout(
        yaxis=dict(range=[0, df_plot['Preço'].max()]),
        yaxis_title='Receita',
        xaxis_title='Categoria',
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False,
        uniformtext_minsize=10,
        uniformtext_mode='hide'
    )
    
    return fig