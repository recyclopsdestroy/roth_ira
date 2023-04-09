from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import json, urllib
import pandas as pd
import numpy as np
import flask
from sankeydata import calc_data


f_app = flask.Flask(__name__)
app = Dash(__name__, server=f_app)
# app = Dash(__name__)

app.layout = html.Div([
    html.H4('Dice Outcome Flow'),
    dcc.Graph(id="graph"),
    html.H4('Dice Distribution'),
    dcc.Graph(id = "bar"),
    html.P("dice_start"),
    dcc.Slider(id='dice_start', min=0, max=6, 
               value=1, step=1),
    html.P("dice stop"),
    dcc.Slider(id='dice_stop', min=0, max=6, 
               value=6, step=1),
    html.P("n dice"),
    dcc.Slider(id='n_dice', min=1, max=8, 
               value=2, step=1)
])

@app.callback(
    Output("graph", "figure"), 
    Output("bar", "figure"),
    Input("dice_start", "value"),
    Input("dice_stop", "value"),
    Input("n_dice", "value"))
def display_sankey(dice_start,dice_stop,n_dice):
    
    feed = calc_data(6, dice_start,dice_stop,n_dice)

    dice_obj = feed['data']
    bar_data = dice_obj.summary[n_dice]

    bar_fig = px.bar(bar_data, x = 'result', y = 'probability')

    links_dict = feed['links']

    df = pd.DataFrame(links_dict)
    df['frac_label'] = np.nan
    targets = df['target'].unique()
    for target in targets:
      df.loc[df['target'] == target, 'frac_label'] = df.loc[df['target'] == target, 'value'].sum()/df['value'].sum()
    node_values = (df['frac_label'].drop_duplicates()*100).round(2).to_list()
    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = feed['labels'],
      color = "blue",
      customdata = node_values,
      hovertemplate = "Probability: %{customdata}%"
    ),
    link = dict(
      source = links_dict["source"],
      target = links_dict["target"],
      value = links_dict["value"],#,
      hovertemplate = 'the value is %{links_dict["value"]}'
  ))])
    fig.update_layout(title_text="dice outcomes", font_size=10)
    fig.update_layout(height = 750)
    return fig, bar_fig
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