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
        hover_data={
            'Receita Formatada': True,
            'Preço': False,
            'lat': False,
            'lon': False
        },
        zoom=3.2,
        height=650,
        size_max=60,
        mapbox_style='carto-positron',
        color_continuous_scale='Viridis'
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_showscale=False
    )

    return fig
