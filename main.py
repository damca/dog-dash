import plotly.express as px
import os
import pandas as pd
from datetime import datetime, timedelta
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import flask

app = dash.Dash(__name__)
server = app.server

# serve image
# https://github.com/plotly/dash/issues/71
image_dir = './ims/'
static_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
@app.server.route('/static/<resource>')
def serve_image(resource):
    return flask.send_from_directory(static_path, resource)

import multiprocessing
from listen_keys import conn, start
p1 = multiprocessing.Process(target=start)
p1.start()

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src='/static/dog.jpg',
                            id="dog-image",
                            style={
                                "height": "100px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "Yalli's Recent Activity",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "The Doody Cycle", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Learn More", id="learn-more-button"),
                            href="https://en.wikipedia.org/wiki/German_shepherd",
                        )
                    ],
                    className="one-third column",
                    id="learn-button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.P(id='placeholder'),
                dcc.Interval(id='interval-component', interval=30000, n_intervals=0),
                html.Div(
                    [html.H5("Last Pee"), html.H6(id='peetime')],
                    id="pee",
                    className="mini_container",
                ),
                html.Div(
                    [html.H5("Last Poo"), html.H6(id='pootime')],
                    id="poo",
                    className="mini_container",
                ),
                html.Div(
                    [
                    html.P("Filter by type:", className="control_label"),
                    dcc.RadioItems(
                        id="type-selector",
                        options=[
                            {"label": "Any", "value": "A"},
                            {"label": "Nadda", "value": "0"},
                            {"label": "Pee ", "value": "1"},
                            {"label": "Doo-doo ", "value": "2"},
                        ],
                        value="A",
                        labelStyle={"display": "inline-block"},
                        className="dcc_control",
                        ),
                    ],
                    className="pretty_container",
                    id="filter-options",
                    ),
            ],
            id="info-container",
            className="row flex-display",
        ),
        html.Div(
            [dcc.Graph(id="scat-plot")],
            id="scat-plot-container",
            className="pretty_container",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


lut = {'0': 'blue', '1': 'red', '2': 'green'}
pfmt = '%Y-%m-%d %H:%M:%S.%f'
fmt = '%I:%M %p\n%m-%d-%Y'

def load_df():
    global df, firsttime, lasttime, lastpeet, lastpeed, lastpoot, lastpood
    df = pd.read_sql_query("SELECT * from scat", conn)
    df['y'] = 1
    df['size'] = 10
    df['key'] = df['key'].astype(str)  # make categorical

    firsttime, lasttime = datetime.strptime(df.time.min(), pfmt), datetime.strptime(df.time.max(), pfmt)
    lastpee = datetime.strptime(df[df.key == '1'].iloc[-1].time, pfmt)
    lastpeet, lastpeed = lastpee.strftime(fmt).split('\n')
    lastpoo = datetime.strptime(df[df.key == '2'].iloc[-1].time, pfmt)
    lastpoot, lastpood = lastpoo.strftime(fmt).split('\n')

    df = df.sort_values(by='key')  # so that 0 appears before 1 in legend

load_df()

# having async "load_df" was causing problems.
# make a placeholder that reloads df, then trigger other callbacks.
@app.callback(
        Output('placeholder', 'children'),
        [Input('interval-component', 'n_intervals')],
)
def reload(click):
    load_df()
    return ''

@app.callback(
    Output("peetime", "children"),
    [Input("interval-component", "n_intervals")],
)
def update_peetime(click):
    return [lastpeet, html.Br(), lastpeed]

@app.callback(
    Output("pootime", "children"),
    [Input("interval-component", "n_intervals")],
)
def update_pootime(click):
    return [lastpoot, html.Br(), lastpood]


@app.callback(
    Output("scat-plot", "figure"),
    [Input("type-selector", "value")]
)
def make_scat(typ):
    kwargs = dict(x='time', y='y', size='size', height=300, range_x=[firsttime, lasttime])
    if typ != 'A':
        dfa = df[df.key == typ]
    else:
        dfa = df
        kwargs['color'] = 'key'
    fig = px.scatter(dfa, **kwargs)
    if typ != 'A':
        fig.update_traces(mode='markers', marker_color=lut[typ])
    fig.update_xaxes(showline=True, linewidth=2, showgrid=False, linecolor='black', title_text='Time')
    fig.update_yaxes(showline=True, linewidth=2, showgrid=False, linecolor='black', range=(0.5, 1.5), showticklabels=False, title_text='Event')
    fig.update_layout(legend_title_text='Eliminate', title='Scat-ter Plot', xaxis_tickformat='%I:%m %p <br>%d-%B')
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(debug=False, port=5000, host='0.0.0.0')
