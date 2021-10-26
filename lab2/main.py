# https://dash.plotly.com/basic-callbacks
# https://dash-bootstrap-components.opensource.faculty.ai/docs/components/list_group/
# https://bootstrap-4.ru/docs/5.1/layout/columns/

# http://127.0.0.1:8050/

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from distribution import generate_information_flow

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.layout = html.Div([
    html.H1(children='Лабораторная работа №2'),
    html.H2(children='Моделирование информационных потоков в системах моделирования'),

    html.Hr(className="my-2"),

    html.Div([
        html.Div([
            dbc.Label('Кол-во cсобытий N', style={'width': '200px'}),
            dbc.Input(id='my-input1',  placeholder='N', value=1000, className="col")
        ], className='row justify-content-start'),
        html.Div([
            dbc.Label('Параметр alfa', style={'width': '200px'}),
                dbc.Input(id='my-input2', placeholder='a', value=0.50, className="col")
        ], className='row justify-content-start'),
        html.Div([
            dbc.Label("Параметр beta", style={'width': '200px'}),
            dbc.Input(id='my-input3',  placeholder="n", value=1.50, className="col")
        ], className='row justify-content-start'),
        html.Div([
            dbc.Label("Параметр q", style={'width': '200px'}),
            dbc.Input(id='my-input4',  placeholder="alfa", value=11.50, className="col")
        ], className='row justify-content-start'),
        html.Div([
            dbc.Label("Время t", style={'width': '200px'}),
            dbc.Input(id='my-input5',  placeholder="alfa", value=300, className="col")
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
    State('my-input4', 'value'),
    State('my-input5', 'value'))
def generate(_, N, alfa, beta, q, t):
    information_flow = generate_information_flow(int(N), float(alfa), float(beta), float(q), int(t))
    return (
        information_flow['graph'],
        generate_table(information_flow['table_header'], information_flow['table_items']),
        generate_informations(information_flow['info']),
    )

if __name__ == '__main__':
    app.run_server()