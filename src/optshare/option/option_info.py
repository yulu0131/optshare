import pandas as pd
import os

option_info = pd.read_csv(os.path.join(os.path.dirname(__file__), "option_info.csv"))

def get_exchange_info() -> pd.DataFrame:
    """Exchange Information

    Returns
    -------
    pandas.DataFrame
        supported Exchange information
    """

    exchange_info = pd.DataFrame(columns=['交易市场名称',
                                          '交易市场'])
    exchange_info['交易市场名称'] = option_info['交易市场名称'].unique()
    exchange_info['交易市场'] = option_info['交易市场'].unique()

    return exchange_info


def get_option_info() -> pd.DataFrame:
    """Option Information

    Returns
    -------
    pandas.DataFrame
        supported option information
    """
    option_info_df = pd.DataFrame(columns=['标的代码',
                                           '期权名称'])
    option_info_df['标的代码'] = option_info['标的代码']
    option_info_df['期权名称'] = option_info['期权名称']

    return option_info_df


def get_meta_data(exchange_name=None) -> pd.DataFrame:
    """
    Parameters
    ----------
    exchange_name : str or None
        Supported exchange name, e.g. 'sse'

    Returns
    -----------
    pandas.DataFrame
        Detailed option information given exchange name, or full information if exchange_name = None
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
