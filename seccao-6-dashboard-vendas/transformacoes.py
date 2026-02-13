import streamlit as st
import pandas as pd

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


@st.cache_data
def receita_mensal(df):
        df_temp = df.copy()
        df_temp['Data da Compra'] = pd.to_datetime(df_temp['Data da Compra'])
        df_mensal = ( 
            df_temp.set_index('Data da Compra')
            .groupby(pd.Grouper(freq='M'))['Preço']
            .sum()
            .reset_index()
        )
        df_mensal['Ano'] = df_mensal['Data da Compra'].dt.year
        df_mensal['Mes'] = df_mensal['Data da Compra'].dt.month_name()
    
        return df_mensal

