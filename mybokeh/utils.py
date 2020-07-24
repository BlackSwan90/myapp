import requests
import pandas as pd
import os
import math
import datetime as dt

import global_storage

from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import LinearAxis, HoverTool, CrosshairTool, ranges
from bokeh.resources import CDN


############### alphavantage
def get_data(from_symbol, to_symbol, API_KEY):
    r = requests.get(
        'https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=' + from_symbol + '&to_symbol=' + to_symbol + '&apikey=' + API_KEY)

    # to get dict: metadata + Time Series
    data_Intraday = r.json()

    return data_Intraday['Time Series FX (Daily)']


def convert_to_df(data):
    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.reset_index()
    df = df.rename(index=str, columns={"index": "date", "1. open": "open", "2. high": "high", "3. low": "low",
                                       "4. close": "close"})
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['date'])

    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)

    return df


####################################


############## yahoo ###############
def convert_to_df_yahoo(data):
    df = pd.DataFrame.from_dict(data)
    df = df.rename(columns={"timestamp": "date"})
    df['date'] = pd.to_datetime(df['date'] / 1000, unit='s')

    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)

    return df


def download_symbol_data(selected_symbol,
                         selected_period,
                         selected_freqtype,
                         period_number,
                         selected_freqnum):
    my_share = share.Share(selected_symbol)

    if selected_period == 'day':
        period_type = share.PERIOD_TYPE_DAY
    elif selected_period == 'week':
        period_type = share.PERIOD_TYPE_WEEK
    elif selected_period == 'month':
        period_type = share.PERIOD_TYPE_MONTH
    elif selected_period == 'year':
        period_type = share.PERIOD_TYPE_YEAR

    if selected_freqtype == 'min':
        freqtype = share.FREQUENCY_TYPE_MINUTE
    elif selected_freqtype == 'hour':
        freqtype = share.FREQUENCY_TYPE_HOUR
    elif selected_freqtype == 'day':
        freqtype = share.FREQUENCY_TYPE_DAY
    elif selected_freqtype == 'week':
        freqtype = share.FREQUENCY_TYPE_WEEK
    elif selected_freqtype == 'month':
        freqtype = share.FREQUENCY_TYPE_MONTH
    print(freqtype)

    if selected_freqnum == '1m':
        freqnum = 1
    elif selected_freqnum == '2m':
        freqnum = 3
    elif selected_freqnum == '5m':
        freqnum = 5
    elif selected_freqnum == '15m':
        freqnum = 15
    elif selected_freqnum == '30m':
        freqnum = 30
    elif selected_freqnum == '60m':
        freqnum = 60
    elif selected_freqnum == '90m':
        freqnum = 90
    elif selected_freqnum == '1h':
        freqnum = 1
    elif selected_freqnum == '1d':
        freqnum = 1
    elif selected_freqnum == '5d':
        freqnum = 5
    elif selected_freqnum == '1w':
        freqnum = 1
    elif selected_freqnum == '1mo':
        freqnum = 1
    elif selected_freqnum == '3mo':
        freqnum = 3

    result = None
    result = my_share.get_historical(period_type,
                                     int(period_number),
                                     freqtype,
                                     freqnum)
    return result


def prepare_plot_bk(source,
                    selected_symbol,
                    price_range,
                    time_range,
                    manual_selection):

    increasing = source.close > source.open
    decreasing = source.close < source.open
    w = 12 * 60 * 60 * 1000
    TOOLS = "pan, wheel_zoom, box_zoom, crosshair, hover, reset, save"
    title =  get_symbol_name(selected_symbol) + ' ( ' + selected_symbol + ' )'

    p = figure(
        x_axis_type='datetime',
        tools=TOOLS,
        plot_width=900,
        plot_height=600,
        title=title,
        x_axis_label='Timeline',
        y_axis_label='Price',
        # x_range=(time_min, time_max),
        # y_range=eval(str(price_range)),
    )

    if manual_selection=='checked':
        time_min = dt.datetime.fromisoformat(time_range[0])
        time_max = dt.datetime.fromisoformat(time_range[1])
        p.x_range = ranges.DataRange1d(p.x_range)
        p.x_range.start = time_min
        p.x_range.end = time_max

        price_range_int = eval(str(price_range))
        p.y_range=ranges.DataRange1d(p.y_range)
        p.y_range.start = price_range_int[0]
        p.y_range.end = price_range_int[1]

    p.xaxis.major_label_orientation = math.pi / 4
    p.axis.axis_label_text_font_style = 'bold'
    p.axis.major_label_text_font_style = 'bold'
    p.axis.axis_line_alpha = 1
    p.axis.axis_line_width = 3.
    p.axis.major_tick_line_width = 2.5
    p.axis.minor_tick_line_width = 1.5
    p.xaxis.major_tick_in = 8
    p.xaxis.minor_tick_in = 5
    p.yaxis.major_tick_in = 8
    p.yaxis.minor_tick_in = 5
    p.axis.major_tick_out = 0
    p.axis.minor_tick_out = 0

    p.xaxis.axis_label_text_font_size = "12pt"
    p.xaxis.major_label_text_font_size = "10pt"

    p.yaxis.axis_label_text_font_size = "12pt"
    p.yaxis.major_label_text_font_size = "10pt"

    # p.add_layout(LinearAxis(), place='right')
    # #a.axis.axis_line_width = 3.
    # p.add_layout(LinearAxis(), place='above')

    p.grid.grid_line_alpha = 0.5
    p.grid.grid_line_color = 'black'

    p.grid.minor_grid_line_width = 1.
    p.grid.minor_grid_line_alpha = 0.2
    p.grid.minor_grid_line_color = 'black'
    p.grid.minor_grid_line_dash = 'dotted'

    p.segment(
        source.date,
        source.high,
        source.date,
        source.low,
        color="black",
    )

    p.vbar(
        source.date[increasing],
        w,
        source.open[increasing],
        source.close[increasing],
        fill_color="#008000",
        line_color="black"
    )

    p.vbar(
        source.date[decreasing],
        w,
        source.open[decreasing],
        source.close[decreasing],
        fill_color="#FF0000",
        line_color="black"
    )

    return p


def get_plot_bk(selected_symbol,
                selected_period,
                selected_freqtype,
                period_number,
                selected_freqnum,
                price_range,
                time_range,
                manual_selection):

    source_raw = download_symbol_data(selected_symbol,
                                      selected_period,
                                      selected_freqtype,
                                      period_number,
                                      selected_freqnum)

    source_df = convert_to_df_yahoo(source_raw)

    plot_bk = prepare_plot_bk(source_df,
                              selected_symbol,
                              price_range,
                              time_range,
                              manual_selection)
    return plot_bk


def get_demo_plot_bk():
    args_plot_bk = get_demo_selection()
    plot_bk = get_plot_bk(**args_plot_bk)
    return plot_bk

def get_symbol_name(selected_symbol):
    df = global_storage.df_symbols
    symbol_name = df.loc[df['Symbol'] == selected_symbol]['Name'].values[0]
    return symbol_name

def get_demo_selection():
    selected_symbol = 'MSFT'
    selected_period = 'day'
    selected_freqtype = 'day'
    period_number = 50
    selected_freqnum = '1d'
    price_range = (150, 250)
    time_min = '2020-03-12 00:00:00'
    time_max = '2020-07-12 00:00:00'
    time_range = [time_min, time_max]
    checked = ''
    dir = {
        'selected_symbol': selected_symbol,
        'selected_period': selected_period,
        'selected_freqtype': selected_freqtype,
        'selected_freqnum': selected_freqnum,
        'period_number': period_number,
        'price_range': price_range,
        'time_range': time_range,
        'manual_selection': checked,
    }
    return dir
