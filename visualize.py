# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go


def showChart(total_hour, df_playback, df_category_rate):

    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    # assume you have a "long-form" data frame
    # see https://plotly.com/python/px-arguments/ for more options
    fig = px.line(df_playback, x=[df_playback.index],
                  y=df_playback.time_minutes)
    fig.update_xaxes(tickformat="%Y-%m-%d", dtick=1 *
                     24*60*60*1000,)  # x軸を1日毎に表示
    fig.update_layout(showlegend=False,
                      title={
                          'text': "日別のYouTube再生時間",
                          'y': 0.95,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'}
                      )

    fig_pie = px.pie(df_category_rate, values=df_category_rate.values,
                     names=df_category_rate.index)
    fig_pie.update_layout(title={
                          'text': "再生履歴のビデオカテゴリの割合",
                          'y': 0.95,
                          'x': 0.5,
                          'xanchor': 'center',
                          'yanchor': 'top'}
                          )

    app.layout = html.Div(children=[
        # html.H6(children=f'合計再生時間:{total_hour}時間'),
        html.Div(children=[
            html.Div(
                children="日付範囲：",
                style={'display': 'inline-block'}
            ),
            dcc.DatePickerRange(
                id='date-range',
                display_format='YYYY-MM-DD',
                min_date_allowed=df_playback.index.min(),
                max_date_allowed=df_playback.index.max(),
                start_date=df_playback.index.min(),
                end_date=df_playback.index.max(),
            )],
            style={'text-align': 'center'}
        ),
        html.Div([
            dcc.Graph(
                id='playback-time-graph',
                figure=fig,
                config={"displayModeBar": False}
            ),
        ], style={'display': 'inline-block', 'width': '50%'}
        ),
        html.Div([
            dcc.Graph(
                id='test',
                figure=fig_pie,
                config={"displayModeBar": False}
            ),
        ], style={'display': 'inline-block', 'width': '50%'}),
    ])

    app.run_server(debug=False)

    @app.callback(
        Output('playback-time-graph', 'figure'),
        Input('date-range', 'start_date'),
        Input('date-range', 'end_date')
    )
    def update_output_div(start_date, end_date):
        set_df = df_playback[start_date: end_date]
        set_fig = px.line(
            set_df, x=[set_df.index], y=set_df['time_minutes'])
        set_fig.update_xaxes(tickformat="%Y-%m-%d",
                             dtick=1*24*60*60*1000)  # x軸を1日毎に表示

        return set_fig


if __name__ == '__main__':
    # import pandas as pd
    # _df = pd.read_csv('./test.csv', parse_dates=['datetime'])
    # # 日付で集計
    # ret = _df.groupby(_df['datetime'].dt.date).sum()
    # # カテゴリーの多い順に並び変え(回数)
    # d_count = _df['category'].value_counts().to_dict()
    # # カテゴリーの多い順に並び変え(割合)
    # d_normalize = _df['category'].value_counts(normalize=True).to_dict()
    # df_normalize = _df['category'].value_counts(normalize=True)
    # df_dict = pd.DataFrame.from_dict(d_normalize, orient='index')
    # a = pd.DataFrame(list(d_normalize.items()),
    #                  columns=['category', 'rate'])
    # print(df_normalize.index.tolist())
    # print(df_normalize.values)
    # # インデックスをdatetimeに変換
    # # ret.index = pd.to_datetime(ret.index)
    # showChart(20, ret, df_normalize)
    pass
