""" Current Financial Option T-type Quotation

For the convenience of future research, Raw data is parsed and re-formulated as T-type quotation.

The format of T-type quotation data:
- date, strike, the latest price of call option, latest price of put option, underlying code, the latest price of underlying, expiry date
"""

import optshare
from datetime import datetime, date
import pandas as pd

class FinancialOption:
    def __init__(self, exchange_name):
        self.exchange_name = exchange_name
        self.underlying_df = optshare.get_current_index()

    def get_expiry_date(self, option_underlying_contract, today):
        if self.exchange_name == "cffex":
            year = int(option_underlying_contract[2:4]) + 2000
            month = int(option_underlying_contract[4:6])
            return str(optshare.get_weekday_in_month(year, month, 3, 5))

        if self.exchange_name == "szse" or "sse":
            start_index = 0
            end_index = 0
            for i in range(len(option_underlying_contract)):
                s = option_underlying_contract[i]
                if s == '购' or s == '沽':
                    start_index = i + 1
                if s == '月':
                    end_index = i
                    break

            expiry_month = int(''.join(option_underlying_contract[start_index:end_index]))

            expiry_date = optshare.get_weekday_in_month(today.year, expiry_month, 4, 3)
            if expiry_date < today:
                expiry_date = optshare.get_weekday_in_month(today.year + 1, expiry_month, 4, 3)
            if expiry_date == date(2023, 1, 25):
                expiry_date = optshare.date(2023, 1, 30)
            return str(expiry_date)

    def _parse_ccfex_contract(self, option_contract):
        # designed for cffex only
        option_contract = option_contract.split('-')
        underlying_code = option_contract[0]
        expiry_date = self.get_expiry_date(underlying_code, today = None)

        return underlying_code, expiry_date

    def get_financial_option(self, underlying_asset_code, current_datetime=None):
        if current_datetime is None:
            current_datetime = optshare.get_market_time(datetime.now())
        else:
            current_datetime = optshare.get_market_time(current_datetime)

        current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M')

        try:
            option_df = optshare.get_current_option(underlying_code=underlying_asset_code)
            underlying_price = self.underlying_df[self.underlying_df["代码"] == underlying_asset_code]['最新价'].values[-1]
        except:
            raise Exception("wrong underlying asset code")

        call_df = option_df[option_df['名称'].str.contains('购')]
        put_df = option_df[option_df['名称'].str.contains('沽')]

        put_df = put_df.sort_values(by='名称')
        call_df = call_df.sort_values(by='名称')

        option_quote = pd.DataFrame(columns=['日期', '行权价',
                                             '看涨合约-最新价', '看跌合约-最新价',
                                             '挂钩标的代码', '挂钩标的-最新价',
                                             '到期日期'])

        option_quote['行权价'] = call_df['行权价'].values
        option_quote['看涨合约-最新价'] = call_df['最新价'].values
        option_quote['看跌合约-最新价'] = put_df['最新价'].values

        option_names = call_df['名称'].values
        option_contracts = call_df['代码'].values.astype(str)

        n = len(option_contracts)
        underlying_asset_codes = [None] * n
        expiry_dates = [None] * n

        if self.exchange_name == 'cffex':
            for i in range(n):
                underlying_asset_codes[i], expiry_dates[i] = self._parse_ccfex_contract(
                    option_contracts[i])
        else:
            today = current_datetime.date()
            for i in range(n):
                expiry_dates[i] = self.get_expiry_date(option_names[i], today)

        option_quote['到期日期'] = expiry_dates
        option_quote['挂钩标的代码'] = underlying_asset_code
        option_quote['日期'] = current_datetime_str
        option_quote['挂钩标的-最新价'] = underlying_price

        return option_quote

    def get_option_quotes(self, current_datetime=None, display = True):
        if current_datetime is None:
            current_datetime = optshare.get_market_time(datetime.now())
        else:
            current_datetime = optshare.get_market_time(current_datetime)

        underlying_codes = optshare.get_meta_data(exchange_name=self.exchange_name)['标的代码'].values.tolist()

        dfs = []

        for underlying_code in underlying_codes:
            if display:
                print("fetch option quotes for ", underlying_code)

            option_df = self.get_financial_option(underlying_code, current_datetime)

            dfs.append(option_df)

        return pd.concat(dfs, ignore_index=True)

def get_financial_option_quotes(exchange_name):
    financial_option = FinancialOption(exchange_name)
    return financial_option.get_option_quotes()

if __name__ == '__main__':
    exchange_names=['sse', 'cffex', 'szse']
    for name in exchange_names:
        f_quotes = get_financial_option_quotes(exchange_name = name)
        f_quotes['挂钩标的代码'] = f_quotes['挂钩标的代码'].apply('="{}"'.format)
        f_quotes.to_csv("test_" + name + ".csv")
