import plotly.express as px

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
        hover_data={'Receita Formatada'},
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
        coloraxis_showscale=False
    )

    return fig


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
        hover_data={
            'Receita Formatada': True,
            'Preço': False
        },
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