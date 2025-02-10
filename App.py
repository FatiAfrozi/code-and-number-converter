import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import Godel
import Paring
import Project

godel = Godel.GodelEncoder()
paring = Paring.ParingEncoder()
project = Project.InstructionDecoder()

def test(x):
    m = godel.encode(x)
    results = []
    for i in m:
        a, bc = paring.decode(i)
        b, c = paring.decode(bc)
        dict = {'a': a, 'b': b, 'c': c}
        results.append(project.decode_instruction(dict))
    return results

def test_r(string):
    dict = project.decode_instruction_reverse(string)
    m = paring.encode(dict['a'], paring.encode(dict['b'], dict['c']))
    return m

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1(" Convert number and code :", className="text-center text-primary mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.RadioItems(
                id='input-type',
                options=[
                    {'label': 'Code', 'value': 'code'},
                    {'label': 'Number', 'value': 'number'}
                ],
                value='code',
                labelStyle={'margin-right': '10px'}
            )
        ], width=12, className="mb-3")
    ]),
    dbc.Row([
        dbc.Col(
            dcc.Textarea(
                id='input-value',
                placeholder='Enter your input ...',
                style={'width': '100%', 'height': 200, 'padding': '10px'}
            ), width=12
        )
    ]),
    dbc.Row([
        dbc.Col(
            dbc.Button('Send', id='submit-button', n_clicks=0, color="primary", className="mt-3 mb-3"), width=12
        )
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='output', className="bg-light p-3"), width=12)
    ])
], fluid=True)

@app.callback(
    Output('output', 'children'),
    Input('submit-button', 'n_clicks'),
    [Input('input-type', 'value'), Input('input-value', 'value')]
)
def update_output(n_clicks, input_type, input_value):
    if n_clicks > 0:
        if input_type == 'code':
            try:
                lines = input_value.split('\n')
                g = [test_r(line.strip()) for line in lines if line.strip()]
                result = godel.decode(g)
            
                return f"Output: {result}"
            except ValueError:
                return "Please send a valid code :("
        elif input_type == 'number':
            try:
                number = int(input_value)
                results = test(number)
                return html.Div([html.Div(f"{res}") for res in results])
            except ValueError:
                return "Please send a valid number :("
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)