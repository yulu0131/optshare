
""" Current Financial Option T-type Quotation

For the convenience of future research, Raw data is parsed and re-formulated as T-type quotation.

The format of T-type quotation data:
- date, strike, the latest price of call option, latest price of put option, underlying code, the latest price of underlying, expiry date
"""

import optshare
from datetime import datetime
import pandas as pd

class FinancialOption:

    def __init__(self, exchange_name, calendar=optshare.Calendar()):
        """ Specify Exchange name, 'cffex', 'sse', or 'szse'

        :param exchange_name: exchange name offering financial options
        :type exchange_name: str
        :param calendar: define transaction calendar
        :type: optshare.Calendar object, default value: optshare.Calendar()
        """
        self.exchange_name = exchange_name
        self.calendar = calendar
        self.underlying_df = optshare.get_current_index()

    def get_expiry_date(self, option_underlying_contract, today):
        """ Given option underlying contract and today's date, return the expiry date of the financial option

        :param option_underlying_contract: option underlying contract name
        :type option_underlying_contract: str
        :param today: today's date
        :type today: datetime.date
        :return: expiry date string
        :rtype: str
        """
        if self.exchange_name == "cffex":
            year = int(option_underlying_contract[2:4]) + 2000
            month = int(option_underlying_contract[4:6])
            expiry_date = optshare.get_weekday_in_month(year, month, 3, 5)

        elif self.exchange_name == "szse" or "sse":
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

        else:
            raise Exception('Wrong Exchange Name Input!')

        if self.calendar.is_holiday(expiry_date):
            expiry_date = self.calendar.next_business_day(expiry_date)

        return str(expiry_date)

    def _parse_cffex_contract(self, option_contract):
        """ Designed for cffex exchange contract only

        :param option_contract: option contract name
        :type option_contract: str
        :return: underlying code, and the corresponding expiry date
        :rtype: tuple[str, str]
        """
        option_contract = option_contract.split('-')
        underlying_code = option_contract[0]
        expiry_date = self.get_expiry_date(underlying_code, today=None)

        return underlying_code, expiry_date

    def get_financial_option(self, underlying_asset_code):
        """ Return option t quote given underlying asset code

        :param underlying_asset_code: underlyng asset code of the financial option
        :type underlying_asset_code: str

        :return: the t-quotes of the selected financial option variety
        :rtype: pandas.DataFrame
        """

        current_datetime = optshare.get_market_time(datetime.now())

        current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M')

        try:
            option_df = optshare.get_current_option(underlying_code=underlying_asset_code)
            underlying_price = self.underlying_df[self.underlying_df["代码"] == underlying_asset_code]['最新价'].values[
                -1]
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

        expiry_dates = [None] * n

        if self.exchange_name == 'cffex':
            underlying_asset_code = [None] * n
            for i in range(n):
                underlying_asset_code[i], expiry_dates[i] = self._parse_cffex_contract(
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

    def get_option_quotes(self, display=True):
        """ Return all option t-quotes in given exchange name

        :param display: Determine whether to display the variety of option quotes when fetching data
        :type display: bool, default True
        :return: Supported financial option t-quotes in given exchange name
        :rtype: pandas.DataFrame
        """

        underlying_codes = optshare.get_meta_data(exchange_name=self.exchange_name)['标的代码'].values.tolist()

        dfs = []

        for underlying_code in underlying_codes:
            if display:
                print("fetch option quotes for ", underlying_code)

            option_df = self.get_financial_option(underlying_code)

            dfs.append(option_df)

        return pd.concat(dfs, ignore_index=True)


def get_financial_option_quotes(exchange_name, calendar = optshare.Calendar(), display=True):
    """ Financial option quotes

    :param exchange_name: exchange name
    :type exchange_name: str
    :param calendar: define transaction calendar, default optshare.Calendar
    :type calendar: optshare.Calendar object
    :param display: Determine whether to display the variety of option quotes when fetching data
    :return: Supported financial option t-quotes in given exchange name
    :rtype: pandas.DataFrame
    """
    financial_option = FinancialOption(exchange_name, calendar)
    return financial_option.get_option_quotes(display=display)


if __name__ == '__main__':
    # exchange_names=['sse', 'cffex', 'szse']
    exchange_names = ['cffex']
    for name in exchange_names:
        f_quotes = get_financial_option_quotes(exchange_name=name)
        print(f_quotes)
        # f_quotes['挂钩标的代码'] = f_quotes['挂钩标的代码'].apply('="{}"'.format)
        f_quotes.to_csv("test_" + name + ".csv")
