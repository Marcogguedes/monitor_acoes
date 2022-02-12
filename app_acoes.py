#!/usr/bin/env python
# coding: utf-8

# # Construcao do script para montar o Dashboard

# ### Importando as biblioteca
import streamlit as st
import pandas as pd
import investpy as ip
from datetime import datetime, timedelta
import plotly.graph_objs as go

countries = ['Brazil', 'United States', 'Germany', 'Japan']
intervals = ['Daily', 'Weekly', 'Monthly']

start_date = datetime.today() - timedelta(days=30)
end_date = datetime.today()


# ### Criando uma funcao para consultar os dados
@st.cache
def consultar_acao(stock, country, from_date, to_date, interval):
    df = ip.get_stock_historical_data(stock=stock, country=country, from_date=from_date, to_date=to_date, interval=interval)
    return df


# ### Criando uma funcoo para defernir o formato da data
def format_date(dt, format='%d%m%Y'):
    return dt.strftime(format)

def plotCandleStick(df, acao='ticket'):
    tracel = {
        'x': df.index,
        'open': df.Open,
        'close': df.Close,
        'high': df.High,
        'low': df.Low,
        'type': 'candlestick',
        'name': acao,
        'showlegend': False
    }
    
    data = [tracel]
    layout = go.Layout()
    
    fig = go.Figure(data=data, layout=layout)
    return fig


# ### Iniciando a Criacao do Dashboard

# Criando uma barra lateral
barra_lateral = st.sidebar.empty()

# Inserindo o objeto selecionar Pais na barra lateral
country_select = st.sidebar.selectbox("Selecione o País:", countries)

# Selecionar acoes dos paises de referencia para retornar uma lista de ativos
acoes = ip.get_stocks_list(country=country_select)

# Inserindo o objeto selecionar todos os ativos na barra lateral
stock_select = st.sidebar.selectbox("Selecione as Ações:", acoes)

# Inserindo o objeto e criando o componente de data na barra lateral
from_date = st.sidebar.date_input("De:", start_date)
to_date = st.sidebar.date_input("Para:", end_date)

# Inserindo o objeto selecionar intevalos na barra lateral
interval_select = st.sidebar.selectbox("Selecione o invervalo:", intervals)

carregar_dados = st.sidebar.checkbox('Carregar Dados')

# ### Criando os elementos centrais do Dashboard

# Inserindo o titulo 
st.title('Monitor de Ações')

# Inserindo o cabecalho
st.header('Ações')

st.subheader('Visualização Gráfica')

# Inserindo o grafico de candle
grafico_candle = st.empty()

# Inserindo o grafico de linha
grafico_line = st.empty()

# Realizando a verificacao da data
if from_date > to_date:
    st.sidebar.error('Data de inicio maior do que a data final')
else:
    df = consultar_acao(stock_select, country_select, format_date(from_date), format_date(to_date), interval_select)
    try:
        fig = plotCandleStick(df)
        grafico_candle = st.plotly_chart(fig)
        grafico_line = st.line_chart(df.Close)
        
        if carregar_dados:
            st.subheader('Dados')
            dados = st.dataframe(df)
    except Exception as e:
        st.error(e)

# # Fim
