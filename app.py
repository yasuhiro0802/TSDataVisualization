import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import os

filename = os.listdir('./sample_csv')
column_dict = {i: pd.read_csv('./sample_csv/' + i).columns.tolist()[1:] for i in os.listdir('./sample_csv')}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='select-csv',
                options=[{'label': i, 'value': i} for i in filename],
                value=filename[0]
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='select-column',
                options=[{'label': i, 'value': i} for i in column_dict[filename[0]]],
                value=column_dict[filename[0]][0]
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),

    html.Hr(),

    dcc.Graph(id='graph0')
])


@app.callback(
    Output('select-column', 'options'),
    [Input('select-csv', 'value')])
def set_column_options(selected_csv):
    if not selected_csv:
        return [{'label': i, 'value': i} for i in column_dict[filename[0]]]
    return [{'label': i, 'value': i} for i in column_dict[selected_csv]]


@app.callback(
    Output('graph0', 'figure'),
    [Input('select-csv', 'value'),
     Input('select-column', 'value')])
def update_graph(csv_name, column_name):
    try:
        df = pd.read_csv('./sample_csv/' + csv_name)[column_name]
    except:
        return {}

    return {
        'data': [dict(
            x=df.index,
            y=df,
            text=column_name,
            mode='lines',
            marker={
                'size': 8,
                # 'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'blue'}
            }
        )],
        'layout': dict(
            xaxis={
                'title': csv_name + '-' + column_name
            },
            margin={'l': 40, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)