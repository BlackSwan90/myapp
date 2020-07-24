import datetime
import pprint
import requests
import yaml
from yahoo_finance_api2.exceptions import YahooFinanceError
import pandas as pd

# Valid frequencies: [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]

class Share(object):

    def __init__(self, symbol):
        self.symbol = symbol

    def get_historical(self, myend, frequency):
        data = self._download_symbol_data(myend, frequency)

        if 'timestamp' not in data:
            return None

        return_data = {
            'timestamp': [x * 1000 for x in data['timestamp']],
            'open': data['indicators']['quote'][0]['open'],
            'high': data['indicators']['quote'][0]['high'],
            'low': data['indicators']['quote'][0]['low'],
            'close': data['indicators']['quote'][0]['close'],
            'volume': data['indicators']['quote'][0]['volume']
        }

        return return_data


    def _set_time_frame(self, myend):
        end_time = myend # as timestamp
        start_time = myend - 86400*30 #one month in s
        return int(start_time), int(end_time)


    def _download_symbol_data(self, myend, frequency):
        start_time, end_time = self._set_time_frame(myend)
        url = (
            'https://query1.finance.yahoo.com/v8/finance/chart/{0}?symbol={0}'
            '&period1={1}&period2={2}&interval={3}&'
            'includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&'
            'region=US&crumb=t5QZMhgytYZ&corsDomain=finance.yahoo.com'
        ).format(self.symbol, start_time, end_time, frequency)

        resp_json = requests.get(url).json()

        if self._is_yf_response_error(resp_json):
            self._raise_yf_response_error(resp_json)
            return

        data_json = resp_json['chart']['result'][0]

        return data_json


    def _is_yf_response_error(self, resp):
        return resp['chart']['error'] is not None


    def _raise_yf_response_error(self, resp):
        raise YahooFinanceError(
            '{0}: {1}'.format(
                resp['chart']['error']['code'],
                resp['chart']['error']['description']
            )
        )


def convert_to_df_yahoo(data):
    df = pd.DataFrame.from_dict(data)
    df = df.rename(columns={"timestamp": "date"})
    df['date'] = pd.to_datetime(df['date'] / 1000, unit='s')

    df.open = df.open.astype(float)
    df.close = df.close.astype(float)
    df.high = df.high.astype(float)
    df.low = df.low.astype(float)

    return df


my_share = Share('GOOG')

mymonths = 5#(2020-2004)*12
mynow = datetime.datetime.fromisoformat('2020-07-20')
mynow_timestamp = mynow.timestamp()
myinterval = 30*24*3600

for i in range(mymonths):
    end_time = mynow_timestamp - i*myinterval
    print(i)
    result = my_share.get_historical(end_time,'30m')
    df = convert_to_df_yahoo(result)
    end_time_date = datetime.datetime.fromtimestamp(end_time)
    end_time_rounded = end_time_date.date()
    filename = end_time_rounded.isoformat()
    df.to_csv(filename + '.csv')