import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

import plotly
from plotly.offline import *
import plotly.graph_objs as go
import plotly.plotly as py
import plotly.offline

df = pd.read_csv('/Users/dshepherd/summary.csv')


def generate_graph(id1, title, series):
    return dcc.Graph(
        id=id1,
        figure={data: series,
                'layout': {
                    'title': title
                }
                }),


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Sky DAT Hybrid Cloud Usage'),
    dcc.Graph(
        id='Sample',
        figure={
            'data': [
                {'x': df["server-volume"], 'y': df['uploadfilecount'], 'type': 'bar', 'name': 'Uploaded Files'},
                {'x': df["server-volume"], 'y': df['downloadfilecount'], 'type': 'bar', 'name': 'Downloaded Files'},
            ],
            'layout': {
                'title': 'CIS Tier Utilisation'

            }
        }),
    generate_table(df)

])

if __name__ == '__main__':
    app.run_server(debug=True)