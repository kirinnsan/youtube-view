# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output


def showChart(total_hour, df):

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    # assume you have a "long-form" data frame
    # see https://plotly.com/python/px-arguments/ for more options
    fig = px.line(df, x=[df.index], y=df.time_minutes)
    fig.update_xaxes(tickformat="%Y-%m-%d", dtick=1*24*60*60*1000)  # x軸を1日毎に表示

    app.layout = html.Div(children=[
        html.H3(children=f'合計再生時間:{total_hour}時間'),
        html.Div(children=[
            html.Div(
                children="日付範囲",
            ),
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=df.index.min(),
                max_date_allowed=df.index.max(),
                start_date=df.index.min(),
                end_date=df.index.max(),
            ),
        ]),
        html.H4(children='日別のYouTube再生時間', style={
            'textAlign': 'center',
        }),
        dcc.Graph(
            id='playback-time-graph',
            figure=fig,
        ),
    ])

    @app.callback(
        Output('playback-time-graph', 'figure'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date')
    )
    def update_output_div(start_date, end_date):
        set_df = df[start_date: end_date]
        set_fig = px.line(
            set_df, x=[set_df.index], y=set_df['time_minutes'])
        set_fig.update_xaxes(tickformat="%Y-%m-%d",
                             dtick=1*24*60*60*1000)  # x軸を1日毎に表示

        return set_fig

    app.run_server(debug=True)


if __name__ == '__main__':
    # import pandas as pd
    # _df = pd.read_csv('./test.csv', parse_dates=['datetime'])
    # 日付で集計
    # ret = _df.groupby(_df['datetime'].dt.date).sum()
    # インデックスをdatetimeに変換
    # ret.index = pd.to_datetime(ret.index)
    # showChart(20, ret)
    pass
