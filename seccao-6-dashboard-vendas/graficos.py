import plotly.express as px
import plotly.graph_objects as go


# ==========================================================
# FUNÇÃO AUXILIAR - FORMATAÇÃO EM REAL (PADRÃO BR)
# ==========================================================
def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ==========================================================
# RECEITA POR ESTADO (TOP 5)
# ==========================================================
def grafico_barra_receita_estado(df):

    df_plot = (
        df.sort_values("Preço", ascending=False)
        .head(5)
        .copy()
    )

    df_plot["Receita_Formatada"] = df_plot["Preço"].apply(formatar_real)

    fig = px.bar(
        df_plot,
        x="Local da compra",
        y="Preço",
        text="Receita_Formatada",
        height=520
    )

    fig.update_traces(
        textposition="outside",
        customdata=df_plot[["Receita_Formatada"]],
        hovertemplate=
        "<b>Estado:</b> %{x}<br>" +
        "<b>Receita Total:</b> %{customdata[0]}" +
        "<extra></extra>"
    )

    fig.update_layout(
        title="Top 5 Estados por Receita",
        xaxis_title="Estado",
        yaxis_title="Receita (R$)",
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )

    return fig

# ==========================================================
# MAPA - RECEITA POR ESTADO
# ==========================================================
def grafico_receita_estado_mapa(df):

    df_plot = df.copy()

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
        zoom=3.6, 
        height=520,
        size_max=65,
        mapbox_style='carto-positron',
        color_continuous_scale='viridis'
    )

    fig.update_traces(
        marker=dict(
            opacity=0.85
        ),
        hovertemplate=
        "<b>%{hovertext}</b><br>" +
        "Receita Total: %{customdata[0]}" +
        "<extra></extra>"
    )

    fig.update_layout(
        mapbox=dict(
            center=dict(lat=-14.2350, lon=-51.9253)
        ),
        margin=dict(l=0, r=0, t=40, b=0),
        coloraxis_colorbar=dict(
            title="Receita (R$)"
        )
    )

    return fig

# ==========================================================
# RECEITA MENSAL
# ==========================================================
def grafico_receita_mensal(df):

    df_plot = df.copy()
    df_plot["Receita_Formatada"] = df_plot["Preço"].apply(formatar_real)

    fig = px.line(
        df_plot,
        x="Data da Compra",
        y="Preço",
        markers=True,
        height=520,
        custom_data=["Receita_Formatada"]
    )

    fig.update_traces(
        hovertemplate=
        "<b>Período:</b> %{x|%m/%Y}<br>" +
        "<b>Receita:</b> %{customdata[0]}" +
        "<extra></extra>"
    )

    fig.update_layout(
        title="Evolução da Receita Mensal",
        xaxis_title="Período",
        yaxis_title="Receita (R$)",
        margin=dict(l=0, r=0, t=50, b=0)
    )

    return fig

# ==========================================================
# RECEITA POR CATEGORIA (TOP 7)
# ==========================================================
def grafico_receita_categoria(df):

    df_plot = df.head(7).copy()
    df_plot["Receita_Formatada"] = df_plot["Preço"].apply(formatar_real)

    fig = px.bar(
        df_plot,
        x="Categoria do Produto",
        y="Preço",
        text="Receita_Formatada",
        height=520
    )

    fig.update_traces(
        textposition="outside",
        customdata=df_plot[["Receita_Formatada"]],
        hovertemplate=
        "<b>Categoria:</b> %{x}<br>" +
        "<b>Receita Total:</b> %{customdata[0]}" +
        "<extra></extra>"
    )
    max_vlaue = df_plot['Preço'].max()
    fig.update_layout(
        title="Top 7 Categorias por Receita",
        xaxis_title="Categoria",
        yaxis=dict(range=[0, max_vlaue * 1.15]),
        yaxis_title="Receita (R$)",
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )

    return fig

# ==========================================================
# RECEITA POR VENDEDOR
# ==========================================================
def grafico_receita_vendedores(df):

    df_plot = df.head(7).copy()
    df_plot["Receita_Formatada"] = df_plot["Receita_Total"].apply(formatar_real)

    fig = px.bar(
        df_plot,
        x="Receita_Total",
        y="Vendedor",
        orientation="h",
        text="Receita_Formatada",
        height=520
    )

    fig.update_traces(
        textposition="outside",
        customdata=df_plot[["Receita_Formatada"]],
        hovertemplate=
        "<b>Vendedor:</b> %{y}<br>" +
        "<b>Receita Total:</b> %{customdata[0]}" +
        "<extra></extra>"
    )
    max_value = df_plot["Receita_Total"].max()
    fig.update_layout(
        title="Top 7 Vendedores por Receita",
        xaxis=dict(range=[0, max_value * 1.15]),
        xaxis_title="Receita (R$)",
        yaxis_title="Vendedor",
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )

    return fig

# ==========================================================
# QUANTIDADE DE VENDAS POR VENDEDOR
# ==========================================================
def grafico_vendas_vendedores(df):

    df_plot = df.head(7).copy()

    fig = px.bar(
        df_plot,
        x="Quantidade_Vendas",
        y="Vendedor",
        orientation="h",
        text="Quantidade_Vendas",
        height=520
    )

    fig.update_traces(
        textposition="outside",
        hovertemplate=
        "<b>Vendedor:</b> %{y}<br>" +
        "<b>Quantidade de Vendas:</b> %{x}" +
        "<extra></extra>"
    )
     
    fig.update_layout(
        title="Top 7 Vendedores por Volume de Vendas",
        yaxis_title="Vendedor",
        xaxis_title="Quantidade de Vendas",
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )

    return fig

# ==========================================================
# CURVA DE PARETO
# ==========================================================
def grafico_pareto(df):

    fig = go.Figure()

    fig.add_bar(
        x=df["Vendedor"],
        y=df["Receita_Total"],
        name="Receita"
    )

    fig.add_scatter(
        x=df["Vendedor"],
        y=df["%_Acumulado"],
        name="% Acumulado",
        yaxis="y2"
    )

    fig.update_layout(
        title="Curva de Pareto - Concentração de Receita",
        yaxis=dict(title="Receita (R$)"),
        yaxis2=dict(
            title="% Acumulado",
            overlaying="y",
            side="right"
        ),
        hovermode="x unified",
        height=520
    )

    return fig

# ==========================================================
# DISTRIBUIÇÃO DE PREÇOS (HISTOGRAMA)
# ==========================================================
def grafico_histograma(df):

    df_plot = df.copy()

    fig = px.histogram(
        df_plot,
        x="Preço",
        nbins=30,
        height=520
    )

    fig.update_traces(
        hovertemplate=
        "<b>Faixa de Preço:</b> R$ %{x:,.2f}<br>" +
        "<b>Quantidade de Vendas:</b> %{y}" +
        "<extra></extra>"
    )

    fig.update_layout(
        title="Distribuição de Vendas por Faixa de Preço",
        xaxis_title="Preço (R$)",
        yaxis_title="Quantidade de Vendas",
        bargap=0.05,
        margin=dict(l=0, r=0, t=50, b=0)
    )

    return fig
