# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px


def showChart(total_hour, df):

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    # assume you have a "long-form" data frame
    # see https://plotly.com/python/px-arguments/ for more options
    fig = px.line(df, x=[df.index], y=df.time_minutes)
    fig.update_xaxes(tickformat="%Y-%m-%d", dtick=1*24*60*60*1000)  # x軸を1日毎に表示

    app.layout = html.Div(children=[
        html.H1(children='YouTube再生履歴'),
        html.H3(children=f'合計再生時間:{total_hour}時間'),
        # html.Div(children=f'合計再生時間:{total_hour}時間'),
        dcc.DatePickerRange(
            id='date-range',
            min_date_allowed=df.index.min(),
            max_date_allowed=df.index.max(),
            start_date=df.index.min(),
            end_date=df.index.max(),
        ),
        dcc.Graph(
            id='example-graph',
            figure=fig,
        ),
    ])

    app.run_server(debug=True)


if __name__ == '__main__':
    # import pandas as pd
    # df = pd.read_csv('./test.csv', header=0, parse_dates=['datetime'])
    # ret = df.groupby(df['datetime'].dt.date).sum()
    # print(ret)
    # showChart(20, ret)
    pass
