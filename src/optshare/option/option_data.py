import json
import requests
import pandas as pd


def get_ccfex_option(underlying_symbol=None) -> pd.DataFrame:
    """ 东方财富网-行情中心-期权市场 https://quote.eastmoney.com/center

    Parameters
    ----------
    underlying_symbol : str or None
        ccfex underlying symbol, e.g. '000300', '000852', '000016'

    Returns
    -----------
    pandas.DataFrame
        current ccfex option information
    """

    url = 'https://futsseapi.eastmoney.com/list/option/221'
    params = {
        'cb': 'aaa_callback',
        'orderBy': 'zdf',
        'sort': 'desc',
        'pageSize': '200000',
        'pageIndex': '0',
        'callbackName': 'aaa_callback',
        'blockName': 'callback',
        '_': '1673341385434'
    }

    if underlying_symbol is not None:
        variety = {'variety': '1'}
        params = {**variety, **params}

        if underlying_symbol == '000300':
            params.update(variety='1')

        elif underlying_symbol == '000852':
            params.update(variety='2')

        elif underlying_symbol == '000016':
            params.update(variety='3')

        else:
            raise Exception('Wrong Underlying Symbol!')

    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find('{'):-1])
    temp_df = pd.DataFrame(data_json['list'])

    ccfex_df = pd.DataFrame(columns=['代码',
                                     '名称',
                                     '最新价',
                                     '涨跌额',
                                     '涨跌幅',
                                     '成交量',
                                     '成交额',
                                     '持仓量',
                                     '行权价',
                                     '剩余日',
                                     '日增',
                                     '昨结',
                                     '今开'])

    ccfex_df['代码'] = temp_df['dm']
    ccfex_df['名称'] = temp_df['name']
    ccfex_df['最新价'] = pd.to_numeric(temp_df['p'], errors='coerce')
    ccfex_df['涨跌额'] = pd.to_numeric(temp_df['zde'], errors='coerce')
    ccfex_df['涨跌幅'] = pd.to_numeric(temp_df['zdf'], errors='coerce').astype(str) + str('%')
    ccfex_df['成交量'] = pd.to_numeric(temp_df['np'], errors='coerce')
    ccfex_df['成交额'] = pd.to_numeric(temp_df['cje'], errors='coerce')
    ccfex_df['持仓量'] = pd.to_numeric(temp_df['ccl'], errors='coerce')
    ccfex_df['行权价'] = pd.to_numeric(temp_df['xqj'], errors='coerce')
    ccfex_df['剩余日'] = pd.to_numeric(temp_df['syr'], errors='coerce')
    ccfex_df['日增'] = pd.to_numeric(temp_df['rz'], errors='coerce')
    ccfex_df['昨结'] = pd.to_numeric(temp_df['zjsj'], errors='coerce')
    ccfex_df['今开'] = pd.to_numeric(temp_df['o'], errors='coerce')

    return ccfex_df


def commodity_option_variety(exchange_name) -> dict:
    """
    Parameters
    ----------
    exchange_name : str
        'shfe', 'dce', 'czce'

    Returns
    -----------
    dict
        numbered commodity option variety given exchange name
    """

    if exchange_name == 'shfe':
        symbols = ['cu', 'ru', 'au', 'al', 'zn', 'rb', 'ag']
    elif exchange_name == 'dce':
        symbols = ['m', 'c', 'i', 'pg', 'pp', 'v', 'l', 'p', 'a', 'b', 'y']
    elif exchange_name == 'czce':
        symbols = ['SR', 'CF', 'MA', 'TA', 'RM', 'ZC', 'OI', 'PK']
    else:
        raise Exception('Unsupported Exchange Name!')

    n = len(symbols)
    numbers = list(range(1, n + 1))
    variety_dictionary = {symbols[i]: str(numbers[i]) for i in range(len(symbols))}
    return variety_dictionary


def get_commodity_option(exchange_name=None, underlying_symbol=None) -> pd.DataFrame:
    """ 东方财富网-行情中心-期权市场 https://quote.eastmoney.com/center

    Parameters
    ----------
    exchange_name : str or None
        exchange name, e.g. 'shfe', 'dce', 'czce', 'ine'
    underlying_symbol: str or None
        underlying symbol

    Returns
    -----------
    pandas.DataFrame
        current commodity option information given either exchange name or underlying_symbol
    """

    url = 'https://futsseapi.eastmoney.com/list/'
    params = {
        'cb': 'aaa_callback',
        'orderBy': 'zdf',
        'sort': 'desc',
        'pageSize': '200000',
        'pageIndex': '0',
        'callbackName': 'aaa_callback',
        'blockName': 'callback',
        '_': '1673576240696'
    }

    if exchange_name is not None and underlying_symbol is None:
        if exchange_name in ['shfe', 'dce', 'czce', 'ine']:
            url = url + exchange_name.upper() + 'OPTION'

        else:
            raise Exception("Wrong Exchange Name Input!")

    elif exchange_name is None and underlying_symbol is not None:
        url = url + 'variety/'
        shfe_varity = commodity_option_variety('shfe')
        dce_varity = commodity_option_variety('dce')
        czce_variety = commodity_option_variety('czce')

        if underlying_symbol in ['cu', 'ru']:
            url = url + 'SHFEOPTION/' + shfe_varity[underlying_symbol]

        elif underlying_symbol in ['au', 'al', 'zn', 'rb', 'ag']:
            url = url + '151/' + shfe_varity[underlying_symbol]

        elif underlying_symbol in ['m', 'c', 'i', 'pg', 'pp', 'v', 'l', 'p', 'a', 'b', 'y']:
            url = url + 'DCEOPTION/' + dce_varity[underlying_symbol]

        elif underlying_symbol in ['SR', 'CF', 'TA', 'MA', 'RM', 'OI', 'PK']:
            url = url + 'CZCEOPTION/' + czce_variety[underlying_symbol]

        elif underlying_symbol == 'sc':
            url = url + 'INEOPTION/1'

    else:
        raise Exception('Please Enter Either Exchange Name or Underlying Symbol!')

    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find('{'):-1])
    temp_df = pd.DataFrame(data_json['list'])

    option_df = pd.DataFrame(columns=['代码',
                                      '名称',
                                      '最新价',
                                      '涨跌额',
                                      '涨跌幅',
                                      '成交量',
                                      '成交额',
                                      '持仓量',
                                      '行权价',
                                      '剩余日',
                                      '日增',
                                      '昨结',
                                      '今开'])

    option_df['代码'] = temp_df['dm']
    option_df['名称'] = temp_df['name']
    option_df['最新价'] = pd.to_numeric(temp_df['p'], errors='coerce')
    option_df['涨跌额'] = pd.to_numeric(temp_df['zde'], errors='coerce')
    option_df['涨跌幅'] = pd.to_numeric(temp_df['zdf'], errors='coerce').astype(str) + str('%')
    option_df['成交量'] = pd.to_numeric(temp_df['np'], errors='coerce')
    option_df['成交额'] = pd.to_numeric(temp_df['cje'], errors='coerce')
    option_df['持仓量'] = pd.to_numeric(temp_df['ccl'], errors='coerce')
    option_df['日增'] = pd.to_numeric(temp_df['rz'], errors='coerce')
    option_df['昨结'] = pd.to_numeric(temp_df['zjsj'], errors='coerce')
    option_df['今开'] = pd.to_numeric(temp_df['o'], errors='coerce')

    return option_df


def get_current_option(underlying_code=None, exchange_name=None) -> pd.DataFrame:
    """ 东方财富网-行情中心-期权市场 https://quote.eastmoney.com/center

    Parameters
    ----------
    underlying_code: str or None
        option underlying code
    exchange_name: str or None
        exchange name, e.g. 'ccfex'

    Returns
    -----------
    pandas.DataFrame
        option information given underlying code or exchange name, if neither of them are given, return all current trading options
    """

    url = 'https://66.push2.eastmoney.com/api/qt/clist/get'
    params = {
        'cb': 'jQuery11240028745663294216683_1673331486150',
        'pn': '1',
        'pz': '200000',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:10,m:140,m:141,m:151,m:163',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f28,f11,f62,f128,f136,f115,f152,f133,f108,f163,f161,f162',
        '_': '1673331486214'
    }

    if underlying_code is None and exchange_name is None:
        url = 'https://98.push2.eastmoney.com/api/qt/clist/get'

    elif underlying_code is None and exchange_name is not None:
        if exchange_name == 'ccfex':
            return get_ccfex_option()

        elif exchange_name == 'sse':
            params.update(fs='m:10')

        elif exchange_name == 'szse':
            params.update(fs='m:12')

        elif exchange_name in ['shfe', 'dce', 'czce', 'ine']:
            return get_commodity_option(exchange_name=exchange_name)

        else:
            raise Exception('Wrong Exchange Name Input!')

    elif underlying_code is not None and exchange_name is None:

        # equity
        # underlying code in sse
        if underlying_code in ['510050', '510300', '510500']:
            params.update(fs='m:10+c:' + underlying_code)

        # underlying code in szse
        elif underlying_code in ['159919', '159922', '159915']:
            params.update(fs='m:12+c:' + underlying_code)

        # underlying code in ccfex
        elif underlying_code in ['000300', '000016', '000852']:
            return get_ccfex_option(underlying_code)

        else:
            try:
                return get_commodity_option(underlying_symbol=underlying_code)

            except:
                raise Exception('Wrong Underlying Code!')

    else:
        raise Exception('Unsupported Underlying Symbol or Exchange Name!')

    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find('{'):-2])
    temp_df = pd.DataFrame(data_json['data']['diff'])
    temp_df.columns = [
        '_',
        '最新价',
        '涨跌幅',
        '涨跌额',
        '成交量',
        '成交额',
        '_',
        '_',
        '_',
        '_',
        '_',
        '代码',
        '_',
        '名称',
        '_',
        '_',
        '今开',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '昨结',
        '_',
        '持仓量',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '_',
        '行权价',
        '剩余日',
        '日增'
    ]
    temp_df = temp_df[[
        '代码',
        '名称',
        '最新价',
        '涨跌额',
        '涨跌幅',
        '成交量',
        '成交额',
        '持仓量',
        '行权价',
        '剩余日',
        '日增',
        '昨结',
        '今开'
    ]]
    temp_df['最新价'] = pd.to_numeric(temp_df['最新价'], errors='coerce')
    temp_df['涨跌额'] = pd.to_numeric(temp_df['涨跌额'], errors='coerce')
    temp_df['涨跌幅'] = pd.to_numeric(temp_df['涨跌幅'], errors='coerce')
    temp_df['成交量'] = pd.to_numeric(temp_df['成交量'], errors='coerce')
    temp_df['成交额'] = pd.to_numeric(temp_df['成交额'], errors='coerce')
    temp_df['持仓量'] = pd.to_numeric(temp_df['持仓量'], errors='coerce')
    temp_df['行权价'] = pd.to_numeric(temp_df['行权价'], errors='coerce')
    temp_df['剩余日'] = pd.to_numeric(temp_df['剩余日'], errors='coerce')
    temp_df['日增'] = pd.to_numeric(temp_df['日增'], errors='coerce')
    temp_df['昨结'] = pd.to_numeric(temp_df['昨结'], errors='coerce')
    temp_df['今开'] = pd.to_numeric(temp_df['今开'], errors='coerce')

    return temp_df


if __name__ == '__main__':
    # return exchange dataframe
    all_exchange_strs = ['sse', 'ccfex', 'szse', 'shfe', 'dce', 'czce', 'ine']
    for exchange in all_exchange_strs:
        test_df = get_current_option(exchange_name=exchange)
        print(test_df)

    # return dataframe given each underlying symbol
    sse_symbols = ['510050', '510300', '510500']
    szse_symbols = ['159919', '159922', '159915']
    ccfex_symbols = ['000300', '000016', '000852']
    shfe_symbols = ['cu', 'ru', 'au', 'al', 'zn', 'rb', 'ag']
    dce_symbols = ['m', 'c', 'i', 'pg', 'pp', 'v', 'l', 'p', 'a', 'b', 'y']
    czce_symbols = ['SR', 'CF', 'TA', 'MA', 'RM', 'OI', 'PK']
    ine_symbols = ['sc']
    all_symbols = sse_symbols + szse_symbols + ccfex_symbols + shfe_symbols + dce_symbols + czce_symbols + ine_symbols
    commodity_symbols = shfe_symbols + dce_symbols + czce_symbols + ine_symbols
    for symbol in all_symbols:
        test_df = get_current_option(underlying_code=symbol)
        print(test_df)

