
""" Current Financial Option T-type Quotation

For the convenience of future research, Raw data is parsed and re-formulated as T-type quotation.

The format of T-type quotation data:
- date, strike, the latest price of call option, latest price of put option, underlying code, the latest price of underlying, expiry date
"""

class FinancialOption:
    def __init__(self, exchange_name):
        self.exchange_name = exchange_name

    def get_expiry_date(self):
        pass

    def _parse_ccfex_contract(self):
        pass

    def get_financial_option(self):
        pass

    def get_option_quotes(self):
        pass


def get_financial_option_quotes(exchange_name):
    financial_option = FinancialOption(exchange_name)
    return financial_option.get_option_quotes()

if __name__ == '__main__':

    t_quotes = get_financial_option_quotes(exchange_name="sse")
    print(t_quotes)



