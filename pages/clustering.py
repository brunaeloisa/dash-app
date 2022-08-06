
import pandas as pd
import numpy as np
import joblib
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from urllib.request import urlopen

# Dataset
path = 'https://raw.githubusercontent.com/brunaeloisa/dash-app/main/marketing_campaign_treated.csv'
base = pd.read_csv(path, sep=';')

# Seleciona colunas para análise
base2 = base.copy()
drop_cols = ['AcceptedCmp3','AcceptedCmp4','AcceptedCmp5','AcceptedCmp1','AcceptedCmp2','Response','Complain','Recency','NumWebVisitsMonth']
base2 = base.drop(labels=drop_cols, axis=1)

# Retira outliers
base2 = base2[(base2['Income'] < 600000)]
base2 = base2[(base2['Age'] < 90)]
base2 = base2.reset_index(drop=True)

# Transforma valores categóricos em valores numéricos
base2['Education'] = base2['Education'].replace({'Basic': 0, 'Undergraduate': 1, 'Graduate': 2})

# Reescalonamento dos dados
scaler = StandardScaler()
scaler.fit(base2)
X_scaled = scaler.transform(base2)

# Redução da dimensionalidade
pca = PCA(n_components=3)
pca.fit(X_scaled)
X_reduced = pca.transform(X_scaled)

# Guarda em novo DataFrame
reduced_base = pd.DataFrame(X_reduced, columns=['col1','col2','col3'])

# Carrega o modelo treinado
model = joblib.load(urlopen('https://github.com/brunaeloisa/dash-app/blob/master/modelo.sav'))

# Predição dos grupos
base2['Clusters'] = model.predict(X_reduced)

# Gerando os gráficos
order = ['0','1','2','3']
reduced_base['Clusters'] = base2['Clusters'].astype(str)
base2['Clusters'] = base2['Clusters'].astype(str)

# Características
fig11 = px.scatter_3d(reduced_base, x='col1', y='col2', z='col3', title='K-means', color='Clusters', category_orders={'Clusters': order}, opacity=0.8, template="none").update_traces(marker_size=6)

clusters = base2.groupby('Clusters').size()
fig12 = px.bar(clusters, color=['0','1','2','3'], title='Divisão entre clusters', template="none").update_layout(yaxis_title="Número de clientes")

fig13 = px.violin(base2, y='Income', x='Clusters', title='Renda', color='Clusters', category_orders={'Clusters': order}, template="none")

fig14 = px.histogram(base2, x=base2['Dependents'], color='Clusters', title='Número de dependentes', category_orders={'Clusters': order}, barmode='group', template="none")
fig14.update_layout(bargap=0.3, yaxis_title='Número de clientes', xaxis_title='Quantidade de dependentes').update_xaxes(type='category')

fig15 = px.histogram(base2, x=base2['Education'].map({0:"Basic",1:"Undergraduate",2:"Graduate"}), color='Clusters', category_orders={'Clusters': order}, title='Grau de escolaridade', barmode='group', template="none")
fig15.update_layout(bargap=0.3, yaxis_title="Número de clientes", xaxis_title="Escolaridade").update_xaxes(type='category')

# Comportamento
fig16 = px.scatter(base2, x='Spent', y='Income', color='Clusters', category_orders={'Clusters': order}, title='Consumo por renda', template = "none").update_layout(xaxis_title="Spent", yaxis_title="Income")

fig17 = px.box(base2, y='TotalPurchases', x='Clusters', color='Clusters', title='Número de compras', category_orders={'Clusters': order}, template="none")

fig18 = px.histogram(base2, x=base2['TotalAcceptedCmp'], color='Clusters', title='Participações em campanhas', category_orders={'Clusters': order}, barmode='group', template="none")
fig18.update_layout(bargap=0.3, xaxis_title='Número de campanhas aceitas', yaxis_title='Número de clientes').update_xaxes(type='category')

fig19 = px.scatter(base2, x='Income', y='Wines', color='Clusters', category_orders={'Clusters': order}, title='Consumo de vinhos por renda', template="none")
fig19.update_layout(xaxis_title='Renda', yaxis_title='Consumo em vinho')

fig20 = px.box(base2, y='NumDealsPurchases', x='Clusters', color='Clusters', title='Compras com desconto', category_orders={'Clusters': order}, template="none")
fig20.update_layout(yaxis_title='Número de compras com desconto')

graphs3 = {'Clusterização por K-means': fig11, 'Divisão entre clusters': fig12, 'Renda por cluster': fig13, 'Quantidade de dependentes por cluster': fig14,
           'Grau de escolaridade por cluster': fig15}
graphs4 = {'Consumo por renda': fig16, 'Total de compras': fig17, 'Participações em campanhas por cluster': fig18, 'Consumo de vinhos por renda': fig19,
           'Compras com desconto por cluster': fig20}

# Layout
clust0 = html.Div([
    html.H4('Cluster 0', style = {'font-family':'Arial Black', 'text-align':'center', 'padding-bottom':'0.5%'}),
    html.Ul([
        html.Li('Clientes de alta renda;'),
        html.Li('Consumidores assíduos de vinho;'),
        html.Li('Usufruem pouco de descontos;'),
        html.Li('A maioria não possui dependentes.'),
    ], style = {'font-family':'Arial', 'text-align': 'left'})
], style = {'color':'white', 'background':'radial-gradient(#1f77b4, #1c6ba2)', 'border-style':'hidden', 'border-radius':'25px', 
            'width':'23.25%', 'padding':'1% 1.5%'})

clust1 = html.Div([
    html.H4('Cluster 1', style = {'font-family':'Arial Black', 'text-align':'center', 'padding-bottom':'0.5%'}),
    html.Ul([
        html.Li('São a maioria entre os clientes;'),
        html.Li('Clientes com a renda mais baixa;'),
        html.Li('Compram e consomem pouco;'),
        html.Li('A maioria possui ao menos um dependente.'),
    ], style = {'font-family':'Arial', 'text-align': 'left'})
], style = {'color':'white','background':'radial-gradient(#ff7f0e, #e6720d)', 'border-style':'hidden', 'border-radius':'25px', 
            'width': '23.25%', 'padding':'1% 1.5%'})

clust2 = html.Div([
    html.H4('Cluster 2', style = {'font-family':'Arial Black', 'text-align':'center', 'padding-bottom':'0.5%'}),
    html.Ul([
        html.Li('Clientes que compram bastante;'),
        html.Li('Possuem a segunda maior renda média;'),
        html.Li('Utilizam bem as plataformas de venda;'),
        html.Li('Consomem bastante vinho.'),
    ], style = {'font-family':'Arial', 'text-align': 'left'})
], style = {'color':'white', 'background':'radial-gradient(#2ca02c, #289028)', 'border-style':'hidden', 'border-radius':'25px', 
            'width':'23.25%', 'padding':'1% 1.5%'})

clust3 = html.Div([
    html.H4('Cluster 3', style = {'font-family':'Arial Black', 'text-align':'center', 'padding-bottom':'0.5%'}),
    html.Ul([
        html.Li('São a minoria entre os clientes;'),
        html.Li('A maioria possui um ou dois dependentes;'),
        html.Li('Usufruem muito de descontos;'),
        html.Li('Não engajam nas campanhas.'),
    ], style = {'font-family':'Arial', 'text-align': 'left'})
], style = {'color':'white', 'background':'radial-gradient(#d62728, #c12324)', 'border-style':'hidden', 'border-radius': '25px', 
            'width':'23.25%', 'padding':'1% 1.5%'})

fig_dropdown3 = html.Div([
    html.H5('Características', style = {'font-family':'Arial Black', 'text-align':'center', 'margin': '20px 0px 20px 0px'}),
    dcc.Dropdown(
        id='fig_dropdown3',
        placeholder="Selecione o gráfico que deseja visualizar",
        options=[{'label': x, 'value': x} for x in graphs3.keys()],
        style = {'padding': '0px 20px 0px 20px'}
    ), html.Div(id='fig_plot3') 
], style = {'background':'#f3f3f3', 'border-style':'hidden', 'border-radius':'25px', 'width':'48%'})

fig_dropdown4 = html.Div([
    html.H5('Comportamento', style = {'font-family':'Arial Black', 'text-align':'center', 'margin':'20px 0px 20px 0px'}),
    dcc.Dropdown(
        id='fig_dropdown4',
        placeholder="Selecione o gráfico que deseja visualizar",
        options=[{'label': x, 'value': x} for x in graphs4.keys()],
        style = {'padding': '0px 20px 0px 20px'}
    ), html.Div(id='fig_plot4') 
], style = {'background':'#f3f3f3', 'border-style':'hidden', 'border-radius':'25px', 'width':'48%'})

clust = html.Div([clust0, clust1, clust2, clust3], style={'display':'flex', 'flex-direction':'row', 'flex-wrap':'wrap', 'margin':'20px auto 20px', 'justify-content':'space-around'})
graficos = html.Div([fig_dropdown3, fig_dropdown4], style={'display':'flex', 'flex-direction':'row', 'flex-wrap':'wrap', 'margin':'0 auto 20px', 'justify-content':'space-around'})
layout = html.Div([clust, graficos])
