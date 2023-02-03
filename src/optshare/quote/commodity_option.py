""" Current Commodity Option T-type Quotation

For the convenience of future research, Raw data is parsed and re-formulated as T-type quotation.

The format of T-type quotation data:
- date, strike, the latest price of call option, latest price of put option, underlying code, expiry date
"""

import optshare as opt
from datetime import datetime
import pandas as pd
class CommodityOption:
    def __init__(self, exchange_name):
        self.exchange_name = exchange_name

    def get_expiry_date(self):
        pass

    def _parse_commodity_contract(self):
        pass

    def get_commodity_option(self):
        pass

    def get_option_quotes(self):
        pass


def get_commodity_option_quotes(exchange_name):
    commodity_option = CommodityOption(exchange_name)
    return commodity_option.get_option_quotes()

if __name__ == '__main__':

    t_quotes = get_commodity_option_quotes(exchange_name="dce")
    print(t_quotes)



