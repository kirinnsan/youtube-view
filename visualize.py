# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import datetime as dt

import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output


def showChart(df):
    '''入力データをもとにチャートを作成する。'''

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    df_playback_time = aggregate_playback_time(df)

    app.layout = html.Div(children=[
        html.H6(
            children="YouTube再生履歴",
            style={'text-align': 'center',
                   'backgroundColor': 'black',
                   'color': 'white'
                   }
        ),
        html.Div(children=[
            html.Div(
                children="日付範囲：",
                style={'display': 'inline-block'}
            ),
            dcc.DatePickerRange(
                id='date-range',
                display_format='YYYY-MM-DD',
                min_date_allowed=df_playback_time.index.min(),
                max_date_allowed=df_playback_time.index.max(),
                start_date=df_playback_time.index.min(),
                end_date=df_playback_time.index.max(),
            )],
            style={'margin': '10px'},
        ),
        html.Div([
            html.Div(
                id='playback-time-graph',
                style={'display': 'inline-block', 'width': '60%'}
            ),
            html.Div(
                id='video-category-graph',
                style={'display': 'inline-block', 'width': '40%'}
            ),
        ], style={'backgroundColor': 'white', 'margin': '10px', 'text-align': 'center'}
        )
    ])

    @ app.callback(
        Output('playback-time-graph', 'children'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date')
    )
    def update_playback_time_graph(start_date, end_date):
        set_df = df[(df['date_time'] >= dt.datetime.fromisoformat(start_date)) &
                    (df['date_time'] < (dt.datetime.fromisoformat(end_date) + dt.timedelta(days=1)))]
        set_df = aggregate_playback_time(set_df)
        set_fig = px.line(
            set_df, x=[set_df.index], y=set_df['time_minutes'])
        set_fig.update_xaxes(tickformat="%Y-%m-%d",
                             dtick=1*24*60*60*1000)  # x軸を1日毎に表示
        set_fig.update_layout(showlegend=False,
                              title={
                                  'text': "日別YouTube再生時間",
                                  'font': {'size': 20},
                                  'y': 0.95,
                                  'x': 0.5,
                                  'xanchor': 'center',
                                  'yanchor': 'top'},
                              xaxis={'title': None},
                              yaxis={
                                  'title': {'text': '再生時間（分）', 'font': {'size': 18}}}
                              )
        return dcc.Graph(
            figure=set_fig,
            config={"displayModeBar": False},
        )

    @ app.callback(
        Output('video-category-graph', 'children'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date')
    )
    def update_video_category_graph(start_date, end_date):
        set_df = df[(df['date_time'] >= dt.datetime.fromisoformat(start_date)) &
                    (df['date_time'] < (dt.datetime.fromisoformat(end_date) + dt.timedelta(days=1)))]
        set_df = aggregate_video_category(set_df)
        set_fig = px.pie(set_df, values=set_df.values,
                         names=set_df.index)
        set_fig.update_layout(title={
                              'text': "再生履歴のビデオカテゴリ",
                              'font': {'size': 20},
                              'y': 0.95,
                              'x': 0.5,
                              'xanchor': 'center',
                              'yanchor': 'top'},
                              margin={'l': 0, 'r': 0})
        return dcc.Graph(
            figure=set_fig,
            config={"displayModeBar": False},
        )

    app.run_server(debug=False)


def aggregate_playback_time(df):
    '''日別に再生時間を集計'''
    df_result = df.groupby(df['date_time'].dt.date).sum()
    df_result.index = pd.to_datetime(df_result.index)
    return df_result


def aggregate_video_category(df):
    '''カテゴリーの多い順(割合)で集計'''
    df_result = df['video_category_name'].value_counts(normalize=True)
    return df_result


if __name__ == '__main__':
    # _df = pd.read_csv('./test.csv', parse_dates=['date_time'])
    # showChart(_df)
    pass
