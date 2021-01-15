# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


def showChart(df):

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    # assume you have a "long-form" data frame
    # see https://plotly.com/python/px-arguments/ for more options
    fig = px.line(df, x="date_time", y="time_sec")

    app.layout = html.Div(children=[
        html.H1(children='YouTube視聴履歴'),

        html.Div(children='''
            過去1週間の視聴時間の表示.
        '''),

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])

    app.run_server(debug=True)


if __name__ == '__main__':
    showChart()
