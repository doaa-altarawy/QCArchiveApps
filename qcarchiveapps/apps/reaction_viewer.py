import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from qcarchiveapps.app import app
from qcarchiveapps.connection import get_client

## Functions to call on the fly when page loads


def list_collections():
    client = get_client()
    collections = client.list_collections("reactiondataset")

    names = list(client.list_collections("reactiondataset").reset_index()["name"])
    return [{"label": k, "value": k} for k in names]


def get_history_values(name, category):
    client = get_client()

    ds = client.get_collection("reactiondataset", name)

    methods = ds.list_history().reset_index()[category].unique()
    if category == "method":
        return [{"label": k.upper(), "value": k} for k in methods]
    else:
        return [{"label": k, "value": k} for k in methods]


layout = lambda: html.Div(
    [

        # Header
        html.Div(
            [
                html.Img(src="https://qcarchive.molssi.org/images/QCArchiveLogo.png",
                         style={
                             'height': '150px',
                             'float': 'right',
                             'position': 'relative',
                             'bottom': '40px',
                             'left': '50px'
                         }),
                html.H3('Reaction Dataset Viewer',
                        style={
                            'position': 'relative',
                            'top': '0px',
                            'left': '10px',
                            'font-family': 'Dosis',
                            'display': 'inline',
                            'font-size': '6.0rem',
                            'color': '#4D637F'
                        }),
            ],
            # className='row twelve columns',
            style={
                'position': 'relative',
                'right': '15px'
            }),

        # Main selection tool
        # html.Div([
        #     html.Div([
        #         html.P('HOVER over a drug in the graph to the right to see its structure to the left.'),
        #         html.P('SELECT a drug in the dropdown to add it to the drug candidates at the bottom.')
        #     ],
        #              style={'margin-left': '10px'}),
        #     dcc.Dropdown(id='available-rds', options=list_collections(), className='twelve columns'),
        # ],
        #          className='row'),
        html.Div([
            html.Div([
                html.P('First select a reaction dataset to get started:'),
                #     html.P('SELECT a drug in the dropdown to add it to the drug candidates at the bottom.')
            ]),
            dcc.Dropdown(id='available-rds', options=list_collections(), value="S22"),
            html.Div(id='rds-display-value'),
        ]),
        html.Div([
            html.Label('Select methods to display:'),
            dcc.Dropdown(id='rds-available-methods', options=[], multi=True),
            html.Label('Select bases to display:'),
            dcc.Dropdown(id='rds-available-basis', options=[], multi=True),
            # multi=True,
        ]),
        html.Div([
            html.Label('Groupby:'),
            dcc.RadioItems(id='rds-groupby',
                           options=[{
                               "label": x.title(),
                               "value": x
                           } for x in ["method", "basis", "d3"]],
                           value=None),
            html.Label('Metric:'),
            dcc.RadioItems(id='rds-metric',
                           options=[{
                               "label": "UE",
                               "value": "UE"
                           }, {
                               "label": "URE",
                               "value": "URE"
                           }],
                           value="UE"),
            html.Label('Plot type:'),
            dcc.RadioItems(id='rds-kind',
                           options=[{
                               "label": "Bar",
                               "value": "bar"
                           }, {
                               "label": "Violin",
                               "value": "violin"
                           }],
                           value="bar"),
        ],
                 style={'columnCount': 2}),
        dcc.Graph(id='primary-graph')
    ],
    className='container')


@app.callback([
    Output('rds-display-value', 'children'),
    Output('rds-available-methods', 'options'),
    Output('rds-available-basis', 'options')
], [Input('available-rds', 'value')])
def display_value(value):
    display_value = 'You have selected "{}"'.format(value)

    return display_value, get_history_values(value, "method"), get_history_values(value, "basis")


@app.callback(Output('primary-graph', 'figure'), [
    Input('available-rds', 'value'),
    Input('rds-available-methods', 'value'),
    Input('rds-available-basis', 'value'),
    Input('rds-groupby', 'value'),
    Input('rds-metric', 'value'),
    Input('rds-kind', 'value'),
])
def build_graph(dataset, method, basis, groupby, metric, kind):

    client = get_client()

    ds = client.get_collection("reactiondataset", dataset)
    history = ds.list_history(method=method, basis=basis)
    if (method is None) or (basis is None):
        print("")
        return {}

    fig = ds.visualize(method=method, basis=basis, groupby=groupby, metric=metric, kind=kind, return_figure=True)
    return fig
