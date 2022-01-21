# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 16:57:19 2022

@author: csandfort
"""
import dash
from dash import dash_table
from dash_table import DataTable, FormatTemplate
from dash_table.Format import Format, Scheme, Sign, Symbol
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import datetime
from dash.dependencies import Input, Output, State
import dataRetrieval as dr
import portfolioUtilities as portUtils
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import constants
import assetClasses as ac

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

data_table_style_header_dict = {
    "backgroundColor": "#15191e",
    "color": "#e1e5ea",
    "fontWeight": "bold"
}

data_table_style_cell_dict = {
    "backgroundColor": "#272727",
    "color": "#c4cad4",
    'border': '1px solid #737373',
    "padding-left": 8,
    "padding-right": 8,
    "padding-top": 6,
    "padding-bottom": 6,
    "fontSize": "1rem"
}

greenColor = "#77b300"
redColor = 'IndianRed'

intialPortfolio = ac.AssetCollection("Portfolio.csv")

def get_assets_data_table(name, data):
    columns = [
        dict(id='Ticker', name='Ticker'),
        dict(id='Quantity', name='Quantity', type='numeric',
            format={"specifier": ".0f"}),
        dict(id='Entry', name='Entry', type='numeric',
             format={"specifier": "$.2f"}),
         dict(id='Last', name='Last', type='numeric',
              format={"specifier": "$.2f"})
        ]
    
    # columns.extend([dict(id='Last', name='Last', type='numeric',
    #      format={"specifier": "$.2f"}),

    styles = []




    styles.append({
        'if': {
            'filter_query': '{Ticker} = "Cash"',
            'column_id': ['Quantity', "Last"]
        },
        'color': 'transparent',
        'backgroundColor': 'rgb(39, 39, 39)'
    })


    assetCollection = ac.AssetCollection(existing = data)
    
    assetsDataTable = DataTable(
        id="{}_assets_data_table".format(name.replace(" ", "_")),
        data=assetCollection.df.to_dict("records"),
        columns=columns,
        # hidden_columns=['Chg1D_zs', 'Chg1W_zs', 'Chg1M_zs', 'Chg3M', 'Chg3M_zs'],
        css=[{"selector": ".dash-spreadsheet-menu", "rule": "display: none"}],
        sort_action='native',
        style_header=data_table_style_header_dict,
        style_cell=data_table_style_cell_dict,
        style_data_conditional=styles
    )

    return assetsDataTable

app.layout = html.Div(
    [
     dcc.Store(id='portfolio-store',
               data=intialPortfolio.toDict()),
     dbc.Container(
         fluid=True,
         className="px-0",
         children=[
             dbc.Navbar(
                 [
                     html.A(
                         # Use row and col to control vertical alignment of logo / brand
                         dbc.Row(
                             [
                                 dbc.Col(dbc.NavbarBrand(
                                     html.H4("The Macro™ Dashboard® V2"),
                                     className="ml-2")),
                             ],
                             align="center",
                             no_gutters=True,
                         ),
                         href="#",
                     ),
                 ],
                 dark=True,
                 color="primary",
                 sticky="top"
             )
         ]),
     dbc.Container(
         fluid=True,
         children=[

             dbc.Row(
                 [dbc.Col(
                     "side_bar",
                     xs=2,
                     className="dbc_dark"
                 ),
                     dbc.Col(
                         [dbc.Alert("Click the table", id='out', className="pb-3", is_open = True),
                          html.Div("data table", id="portfolio_data_table")
                          ],
                     xs=10,
                     id="main_content"
                 )],
                 className="dbc_dark mt-4"
             )
         ])
     ])


@app.callback([Output("out", "children"), Output("portfolio_data_table", "children")],
              Input('portfolio-store', 'data'))
def portfolio_store_callback(data):
    portfolio_data_table = get_assets_data_table("portfolio", data)
    
    return "", portfolio_data_table
    

if __name__ == '__main__':
    app.run_server(debug=True, port='5435')