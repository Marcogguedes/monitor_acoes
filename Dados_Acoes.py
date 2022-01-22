#!/usr/bin/env python
# coding: utf-8

# # Monitor de Ação

# ### Importando biblioteca

# In[1]:


import investpy as ip


# ### Get Ações

# In[2]:


countries = ['Brazil', 'United States']
acoes = ip.get_stocks_list(country='Brazil')


# In[3]:


acoes


# ### Query Ações

# In[4]:


from datetime import datetime, timedelta


# In[5]:


dt_start = datetime.today() - timedelta(days=30)
dt_end = datetime.today()


# In[6]:


type(dt_start)


# In[7]:


type(dt_end)


# In[8]:


def format_date(dt, format='%d/%m/%Y'):
    return dt.strftime(format)


# In[9]:


type(format_date(dt_end))


# In[10]:


intervals = ['Daily', 'Weekly', 'Monthly']
df = ip.get_stock_historical_data(stock='ENGI4',
                                 country='Brazil',
                                 from_date=format_date(dt_start),
                                 to_date=format_date(dt_end),
                                 interval='Daily')


# In[11]:


df


# ### Plot Candle

# In[12]:


import plotly.graph_objs as go


# In[13]:


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


# In[14]:


fig = plotCandleStick(df)


# In[15]:


fig

