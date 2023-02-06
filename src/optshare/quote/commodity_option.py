""" Current Commodity Option T-type Quotation

For the convenience of future research, Raw data is parsed and re-formulated as T-type quotation.

The format of T-type quotation data:
- date, strike, the latest price of call option, latest price of put option, underlying code, expiry date
"""

import optshare
from datetime import datetime, date
import pandas as pd
class CommodityOption:
    def __init__(self, exchange_name):
        self.exchange_name = exchange_name
        self.calendar = optshare.Calendar()

    def get_expiry_date(self, option_underlying_contract):
        if self.exchange_name == "dce":
            yymm = option_underlying_contract[-4:]
            year = int(yymm[0:2]) + 2000
            month = int(yymm[2:4])
            last_month = optshare.add_months(date(year, month, 1), -1)

            return optshare.get_nth_trading_day(5, last_month.year, last_month.month, self.calendar)

        elif (self.exchange_name == "shfe") or (self.exchange_name == 'ine'):
            yymm = option_underlying_contract[-4:]
            year = int(yymm[0:2]) + 2000
            month = int(yymm[2:4])
            previous_month = optshare.add_months(date(year, month, 1), -1)

            if self.exchange_name == "ine":
                # 原油
                return optshare.get_lastnth_trading_day(13, previous_month.year, previous_month.month, self.calendar)

            return optshare.get_lastnth_trading_day(5, previous_month.year, previous_month.month, self.calendar)

        elif self.exchange_name == "czce":
            ymm = option_underlying_contract[-3:]
            year = int(ymm[0]) + 2020
            month = int(ymm[1:3])
            previous_month = optshare.add_months(date(year, month, 15), -1)
            if year < 2024:
                return optshare.get_nth_trading_day(3, previous_month.year, previous_month.month, self.calendar)
            else:
                i = 0
                if self.calendar.is_business_day(previous_month):
                    i += 1
                while i < 3:
                    previous_month = self.calendar.previous_business_day(previous_month)
                    i += 1
                return previous_month

        else:
            raise Exception("Wrong Exchange Name!")

    def _parse_commodity_contract(self, option_contract):

        import re
        parsed_code = re.split('(\d+)', option_contract)

        underlying_code = parsed_code[0] + parsed_code[1]
        option_strike = float(parsed_code[3])
        expiry_date = self.get_expiry_date(underlying_code)

        return underlying_code, expiry_date, option_strike

    def get_commodity_option(self, underlying_asset_code, current_datetime = None):
        if current_datetime is None:
            current_datetime = optshare.get_market_time(datetime.now())
        else:
            current_datetime = optshare.get_market_time(current_datetime)

        current_datetime_str = current_datetime.strftime('%Y-%m-%d %H:%M')

        try:
            option_df = optshare.get_current_option(underlying_code=underlying_asset_code)
        except:
            raise Exception("Wrong underlying asset code!")

        call_df = option_df[option_df['名称'].str.contains('购')]
        put_df = option_df[option_df['名称'].str.contains('沽')]

        put_df = put_df.sort_values(by='名称')
        call_df = call_df.sort_values(by='名称')

        option_quote = pd.DataFrame(columns=['日期', '行权价',
                                             '看涨合约-最新价', '看跌合约-最新价',
                                             '挂钩标的代码',
                                             '到期日期'])

        option_quote['看涨合约-最新价'] = call_df['最新价'].values
        option_quote['看跌合约-最新价'] = put_df['最新价'].values

        option_contracts = call_df['代码'].values.astype(str)

        n = len(option_contracts)
        underlying_asset_codes = [None] * n
        expiry_dates = [None] * n
        strikes = [None] * n
        for i in range(n):
            underlying_asset_codes[i], expiry_dates[i], strikes[i] = self._parse_commodity_contract(
                option_contracts[i])

        option_quote['行权价'] = strikes
        option_quote['到期日期'] = expiry_dates
        option_quote['挂钩标的代码'] = underlying_asset_codes
        option_quote['日期'] = current_datetime_str

        return option_quote
    def get_option_quotes(self, current_datetime = None, display = True):
        if current_datetime is None:
            current_datetime = optshare.get_market_time(datetime.now())
        else:
            current_datetime = optshare.get_market_time(current_datetime)

        dfs = []
        commodity_option_df = optshare.get_meta_data(exchange_name=self.exchange_name)
        underlying_asset_codes = commodity_option_df['标的代码'].values.tolist()
        code_dict = commodity_option_df.set_index('标的代码').to_dict()['期权名称']
        for underlying_asset_code in underlying_asset_codes:
            if display:
                print("fetch option quotes for ", code_dict[underlying_asset_code])
            dfs.append(self.get_commodity_option(underlying_asset_code, current_datetime))

        return pd.concat(dfs, ignore_index=True)

def get_commodity_option_quotes(exchange_name):
    commodity_option = CommodityOption(exchange_name)
    return commodity_option.get_option_quotes()

if __name__ == '__main__':
    #todo: check csv later, make sure all option expiry dates right
    exchange_names = ['dce', 'shfe', 'czce', 'ine']
    for name in exchange_names:
        t_quotation = get_commodity_option_quotes(exchange_name=name)
        t_quotation.to_csv("test_"+name+".csv")



