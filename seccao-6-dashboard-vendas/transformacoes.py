import streamlit as st

@st.cache_data
def receita_por_estado(df):
    return (
        df.groupby('Local da compra', as_index=False)['Preço']
          .sum()
          .merge(
              df[['Local da compra', 'lat', 'lon']].drop_duplicates(),
              on='Local da compra'
          )
          .sort_values('Preço', ascending=False)
    )
