from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import json, urllib
import pandas as pd
import numpy as np
import flask
from return_data import calc_data as cd
# from  import calc_data


f_app = flask.Flask(__name__)
app = Dash(__name__, server=f_app)
# app = Dash(__name__)

app.layout = html.Div([
    html.H4('Returns'),
    dcc.Graph(id="graph"),
    html.P("contribution year"),
    dcc.Input(id='c_year', value = 2023, type = 'number'),
    html.P("current income"),
    dcc.Input(id='c_income', value = 88000, type = 'number', step = 0.05),
    html.P("retirement year"),
    dcc.Input(id='r_year', value = 2057, type = 'number'),
    html.P("retirement income"),
    dcc.Input(id='r_income', value = 140000, type = 'number', step = 0.05),
    html.P("rate of return"),
    dcc.Input(id='return_rate', value = 0.07, type = 'number', step = 0.005),
    html.P("principle"),
    dcc.Input(id='principle', value = 10000, type = 'number')
])

@app.callback(
    Output("graph", "figure"), 
    Input("c_year", "value"),
    Input("c_income", "value"),
    Input("r_income", "value"),
    Input("r_year", "value"),
    Input("return_rate", "value"),
    Input("principle", "value"))
def display_sankey(c_year, c_income, r_income, r_year, return_rate, principle):
   
    data = cd(contribution = principle
                    , return_rate = return_rate
                    , current_income = c_income
                    , retirement_income = r_income
                    , contr_year = int(c_year)
                    , ret_year = int(r_year))

    fig = px.line(data, x="year", y="return", color='retirement')

    return fig
    # fig.show()
    
    
    
    # url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
    # response = urllib.request.urlopen(url)
    # data = json.loads(response.read()) # replace with your own data source

    # node = data['data'][0]['node']
    # node['color'] = [
    #     f'rgba(255,0,255,{opacity})' 
    #     if c == "magenta" else c.replace('0.8', str(opacity)) 
    #     for c in node['color']]

    # link = data['data'][0]['link']
    # link['color'] = [
    #     node['color'][src] for src in link['source']]

    # fig = go.Figure(go.Sankey(link=link, node=node))
    # fig.update_layout(font_size=10)
    # return fig
if __name__ == "__main__":
  app.run_server(debug=True)