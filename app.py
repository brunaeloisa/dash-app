
import pandas as pd
import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc

from pages import clustering, home
from home import fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9, fig10, graphs, graphs2
from clustering import fig11, fig12, fig13, fig14, fig15, fig16, fig17, fig18, fig19, fig20, graphs3, graphs4

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.validation_layout = html.Div([home.layout])
app.config.suppress_callback_exceptions = True

# Define the navbar structure
def Navbar():
    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("General", href="/")),
                dbc.NavItem(dbc.NavLink("Clustering", href="/clustering"))
            ],
            brand="Customer Personality Analysis",
            brand_href="/",
        ), 
    ])
    return layout

nav=Navbar()

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Div(id='page-content', children=[]), 
    html.P('© 2022 André Varela, Bruna Soares e Ricardo Queiroz', style = {'color':'#9a9a9a','text-align':'center'})
])

# Create the callback to handle multipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return home.layout
    if pathname == '/clustering':
        return clustering.layout
    else:
        return home.layout

# HOME CALLBACKS
@callback(
    Output('fig_plot', 'children'),
    Input('fig_dropdown', 'value')
)
def update_output(fig_name):
    if fig_name == None:
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        return dcc.Graph(figure=fig1)
    else:
        graphs[fig_name].update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        return dcc.Graph(figure=graphs[fig_name])

@callback(
    Output('fig_plot2', 'children'),
    Input('fig_dropdown2', 'value')
)
def update_output(fig_name2):
    if fig_name2 == None:
        fig6.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        return dcc.Graph(figure=fig6)
    else:
        graphs2[fig_name2].update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        return dcc.Graph(figure=graphs2[fig_name2])

# CLUSTERING CALLBACKS
@callback(
    Output('fig_plot3', 'children'),
    Input('fig_dropdown3', 'value')
)
def update_output(fig_name3):
    if fig_name3 == None:
        fig11.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        return dcc.Graph(figure=fig11)
    else:
        graphs3[fig_name3].update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        return dcc.Graph(figure=graphs3[fig_name3])

@callback(
    Output('fig_plot4', 'children'),
    Input('fig_dropdown4', 'value')
)
def update_output(fig_name4):
    if fig_name4 == None:
        fig16.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        return dcc.Graph(figure=fig16)
    else:
        graphs4[fig_name4].update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        return dcc.Graph(figure=graphs4[fig_name4])

if __name__ == '__main__':
    app.run_server(port=8050, debug=False)
