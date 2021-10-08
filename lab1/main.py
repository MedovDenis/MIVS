# https://dash.plotly.com/basic-callbacks
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/list_group/
# https://bootstrap-4.ru/docs/5.1/layout/columns/

# http://127.0.0.1:8050/

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from distribution import generate_distribution

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    html.H1(children='Лабораторная работа №1'),
    html.H2(children='Моделирование случайных величин'),

    html.Hr(className="my-2"),

    html.Div([
        html.Div([
            dbc.Label('Кол-во реализации N', style={'width': '200px'}),
            dbc.Input(id='my-input1',  placeholder='N', value=1000, className="col")
        ], className='row justify-content-start'),
        html.Div([
            dbc.Label('Параметр "a"', style={'width': '200px'}),
                dbc.Input(id='my-input2', placeholder='a', value=2, className="col")
        ], className='row justify-content-start'),
        html.Div([
            dbc.Label("Кол-во интервалов n", style={'width': '200px'}),
            dbc.Input(id='my-input3',  placeholder="n", value=15, className="col")
        ], className='row justify-content-start'),
        html.Div([
            dbc.Label("Параметр alfa", style={'width': '200px'}),
            dbc.Input(id='my-input4',  placeholder="alfa", value=0.02, className="col")
        ], className='row justify-content-start'),
        html.Div([
            dbc.Button(id='submit-button', className='row align-items-right', children="Генерировать", color="primary")
        ], className='row justify-content-start')
    ], className='container'),

    html.Hr(className="my-2"),

    dcc.Graph(id='my-graph', className='col align-self-center', style={'height': '500px'}),

    html.Hr(className="my-2"),

    html.Div(id='info_container', className='container'),

    html.Div(id='table_container')
], className='container')

def generate_table(header, items):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in header])
        ),
        html.Tbody([
            html.Tr([
                html.Td(item) for item in row
            ]) for row in items
        ])
    ], className="table")

def generate_informations(info):
    return html.Div([
        html.Div([
            html.P('{}: {}'.format(item, info[item]))
        ], className='col-2') for item in info 
    ], className='row')

@app.callback(
    Output('my-graph', 'figure'),
    Output('table_container', 'children'),
    Output('info_container', 'children'),
    Input('submit-button', 'n_clicks'),
    State('my-input1', 'value'),
    State('my-input2', 'value'),
    State('my-input3', 'value'),
    State('my-input4', 'value'))
def generate(_, N, a, n, alfa):
    distribution = generate_distribution(int(N), int(a), int(n), float(alfa))
    return (
        distribution['graph'],
        generate_table(distribution['table_header'], distribution['table_items']),
        generate_informations(distribution['info']),
    )

if __name__ == '__main__':
    app.run_server()