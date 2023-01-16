import pandas as pd

option_info = pd.read_csv('option_info.csv')
def get_exchange_info() -> pd.DataFrame:
    """
    Exchange Information
    :return: supported Exchange
    :rtype: pd.DataFrame
    """
    exchange_info = pd.DataFrame(columns=['交易市场名称',
                                          '交易市场'])
    exchange_info['交易市场名称'] = option_info['交易市场名称'].unique()
    exchange_info['交易市场'] = option_info['交易市场'].unique()

    return exchange_info


def get_option_info() -> pd.DataFrame:
    """
    Option Information
    :return: supported option
    :rtype: pd.DataFrame
    """
    option_info_df = pd.DataFrame(columns=['标的代码',
                                           '期权名称'])
    option_info_df['标的代码'] = option_info['标的代码']
    option_info_df['期权名称'] = option_info['期权名称']

    return option_info_df


def get_meta_data(exchange_name=None) -> pd.DataFrame:
    """
    :param exchange_name: Supported exchange name, e.g. sse
    :rtype: str or None
    :return: Detailed option information given exchange name, or full information if exchange_name = None
    :rtype: pd.DataFrame
    """
    supported_exchanges = option_info['交易市场名称'].unique()
    if exchange_name in supported_exchanges:
        return option_info[option_info['交易市场名称'] == exchange_name]
    elif exchange_name is None:
        return option_info
    else:
        raise Exception('Wrong Exchange Name Input!')


if __name__ == '__main__':
    print(get_meta_data())
