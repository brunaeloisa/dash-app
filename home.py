
import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Dataset
path = 'https://raw.githubusercontent.com/brunaeloisa/dash-app/main/marketing_campaign_treated.csv'
base = pd.read_csv(path, sep=';')

content_mark = dcc.Markdown('Projeto de Ciência de Dados')

# CARD DO FATURAMENTO
produtos = base.loc[:,['Wines','Meat','Sweets','Gold','Fish']].sum()
faturamento = produtos.sum()

# CARD QTD DE CLIENTES CADASTRADOS
qtde_clientes = len(base.index)

# CARD QTD DE CAMPANHAS 
num_camp = sum([1 for x in base.columns if 'AcceptedCmp' in x and 'TotalAcceptedCmp' not in x])

# CARD QTD DE RECLAMAÇÕES
num_reclamacoes = base['Complain'].sum()

# Conhecendo os clientes
fig1 = px.pie(names=['Basic', 'Graduate', 'Undergraduate'], values=base.groupby('Education').size(), title='Clientes por grau de escolaridade', template="none")

fig2 = px.pie(names=['Não possui parceiro(a)','Possui parceiro(a)'], values=base.groupby('Partner').size(), title='Relacionamento dos clientes', template="none")

fig3 = px.pie(names=['0','1','2','3'], values=base.groupby('Dependents').size(), title='Quantidade de dependentes', template="none")

fig4 = px.histogram(base, x='Customer_for', title='Tempo de cliente', template="none")

fig5 = px.box(base, x='Age', title='Clientes por Idade', template="none")

# Conhecendo o negócio
produtos = base.loc[:,['Wines','Meat','Sweets','Gold','Fish']].sum()
fig6 = px.bar(produtos, color=['Wines','Meat','Sweets','Gold','Fish'], title='Faturamento por categoria de produto', template="none").update_layout(xaxis_title="Produtos", yaxis_title="Faturamento")

engajamento = base['TotalAcceptedCmp'].value_counts()
fig7 = px.bar(engajamento, color=['0','1','2','3','4'], title='Adesão em campanhas', template="none").update_layout(xaxis_title="Quantidade de participações em campanhas", yaxis_title="Número de clientes")

campanhas = base.loc[:,['AcceptedCmp1','AcceptedCmp2','AcceptedCmp3','AcceptedCmp4','AcceptedCmp5']].sum()
fig8 = px.bar(campanhas, color=['Campanha 1','Campanha 2','Campanha 3','Campanha 4','Campanha 5'], title='Número de participações por campanha', template="none").update_layout(xaxis_title="Campanhas", yaxis_title="Número de participações")

fig9 = px.histogram(base, y='Spent', x='Dependents', color='Dependents', histfunc='sum', template="none", title='Consumo por quantidade de dependentes')
fig9.update_layout(xaxis_title="Quantidade de dependentes", yaxis_title="Consumo", bargap=0.3).update_xaxes(type='category')

fig10 = px.violin(base, y='Spent', x='Education', color='Education', title='Distribuição de consumo por grau de escolaridade', template = "none")

graphs = {'Clientes por grau de escolaridade': fig1, 'Relacionamento dos clientes': fig2, 'Quantidade de dependentes': fig3, 
          'Tempo de cliente': fig4, 'Clientes por Idade': fig5}
graphs2 = {'Faturamento por categoria de produto': fig6, 'Adesão em campanhas': fig7, 'Número de participações por campanha': fig8, 
          'Consumo por quantidade de dependentes': fig9, 'Distribuição de consumo por grau de escolaridade': fig10}

# Layout
card1 = html.Div([
    html.H4('U$ ' +str(faturamento), style = {'font-family':'Arial Black', 'text-align':'center'}),
    html.H5('de Faturamento', style = {'text-align':'center'})
], style = {'color':'black', 'background':'radial-gradient(#9a9a9a, #8f8f8f)', 'border-style':'hidden', 'border-radius':'25px', 
            'width':'23.25%', 'padding':'0.5%'})

card2 = html.Div([
    html.H4(str(qtde_clientes), style = {'font-family':'Arial Black', 'text-align':'center'}),
    html.H5('Clientes', style = {'text-align':'center'})
], style = {'color':'black', 'background':'radial-gradient(#9a9a9a, #8f8f8f)', 'border-style':'hidden', 'border-radius':'25px', 
            'width': '23.25%', 'padding':'0.5%'})

card3 = html.Div([
    html.H4(str(num_camp), style = {'font-family':'Arial Black', 'text-align': 'center'}),
    html.H5('Campanhas de Marketing', style = {'text-align':'center'})
], style = {'color':'black', 'background':'radial-gradient(#9a9a9a, #8f8f8f)', 'border-style':'hidden', 'border-radius':'25px', 
            'width':'23.25%', 'padding':'0.5%'})

card4 = html.Div([
    html.H4(str(num_reclamacoes), style = {'font-family':'Arial Black', 'text-align': 'center'}),
    html.H5('Reclamações', style = {'text-align':'center'})
], style = {'color':'black', 'background':'radial-gradient(#9a9a9a, #8f8f8f)', 'border-style':'hidden', 'border-radius': '25px', 
            'width':'23.25%', 'padding':'0.5%'})

fig_dropdown = html.Div([
    html.H5('Conhecendo os clientes', style = {'font-family':'Arial Black', 'text-align':'center', 'margin': '20px 0px 20px 0px'}),
    dcc.Dropdown(
        id='fig_dropdown',
        placeholder="Selecione o gráfico que deseja visualizar",
        options=[{'label': x, 'value': x} for x in graphs.keys()],
        style = {'padding': '0px 20px 0px 20px'}
    ), html.Div(id='fig_plot') 
], style = {'background':'#f3f3f3', 'border-style':'hidden', 'border-radius':'25px', 'width':'48%'})

fig_dropdown2 = html.Div([
    html.H5('Conhecendo o negócio', style = {'font-family':'Arial Black', 'text-align':'center', 'margin':'20px 0px 20px 0px'}),
    dcc.Dropdown(
        id='fig_dropdown2',
        placeholder="Selecione o gráfico que deseja visualizar",
        options=[{'label': x, 'value': x} for x in graphs2.keys()],
        style = {'padding': '0px 20px 0px 20px'}
    ), html.Div(id='fig_plot2') 
], style = {'background':'#f3f3f3', 'border-style':'hidden', 'border-radius':'25px', 'width':'48%'})

cards = html.Div([card1, card2, card3, card4], style={'display':'flex', 'flex-direction':'row', 'flex-wrap':'wrap', 'margin':'20px auto 20px', 'justify-content':'space-around'})
graficos = html.Div([fig_dropdown, fig_dropdown2], style={'display':'flex', 'flex-direction':'row', 'flex-wrap':'wrap', 'margin':'0 auto 20px', 'justify-content':'space-around'})
layout = html.Div([cards, graficos])