import os
import pandas as pd

def load_symbols():
    # needs to install pip install xlrd to read xlsx files !!!
    #mypath = os.path.join(os.getcwd(), 'mybokeh', 'yh_symbols_selection.xlsx')
    mypath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'mybokeh', 'yh_symbols_selection.xlsx')
    df = pd.read_excel(mypath)
    return df[['Symbol', 'Name']]


def get_selector_list():
    df = load_symbols()
    symbol_name_list = (df['Name'] + ' - ' + df['Symbol']).to_list()
    symbol_list = df['Symbol'].to_list()
    name_list = df['Name'].to_list()
    symbol_name_comb_list = list(zip(symbol_name_list, symbol_list))
    period_list = ['day', 'week', 'month', 'year']
    freqtype_list = ['min', 'hour', 'day', 'week', 'month']
    freqnum_list = ['1m', '2m', '5m', '15m', '30m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
    dir = {
        'symbol_list': symbol_list,
        'name_list': name_list,
        'symbol_name_list': symbol_name_list,
        'symbol_name_comb_list': symbol_name_comb_list,
        'period_list': period_list,
        'freqtype_list': freqtype_list,
        'freqnum_list': freqnum_list,
    }
    global selector_list
    global df_symbols
    selector_list = dir
    df_symbols = df

