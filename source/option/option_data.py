import json
import requests
import pandas as pd


def get_ccfex_option(underlying_symbol=None) -> pd.DataFrame:
    """
    东方财富网-行情中心-期权市场
    https://quote.eastmoney.com/center
    :param underlying_symbol: ccfex underlying symbol, e.g. '000300', '000852', '000016'
    :rtype: str or None
    :return: current ccfex option information
    :rtype: pandas.DataFrame
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
            params.update(variety='1', _='1673514935737')

        elif underlying_symbol == '000852':
            params.update(variety='2', _='1673515386524')

        elif underlying_symbol == '000016':
            params.update(variety='3', _='1673515482877')

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

def get_commodity_option(exchange_name = None, underlying_symbol=None) -> pd.DataFrame:
    """
    东方财富网-行情中心-期权市场
    https://quote.eastmoney.com/center
    :param exchange_name: exchange name, e.g. 'shfe', 'dce', 'czce', 'ine'
    :rtype: str or None
    :param underlying_symbol: underlying symbol
    :rtype: str or None
    :return: current commodity option information given either exchange name or underlying_symbol
    :rtype: pandas.DataFrame
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
        if exchange_name == 'shfe':
            url = url + 'SHFEOPTION'

        elif exchange_name == 'dce':
            url = url + 'DCEOPTION'
            params.update(_ = '1673578133884')
        elif exchange_name == 'czce':
            url = url +'CZCEOPTION'
            params.update(_='1673578133904')

        elif exchange_name == 'ine':
            url = url + 'INEOPTION'
            params.update(_='1673578133929')

        else:
            raise Exception("Wrong Exchange Name Input!")

    elif exchange_name is None and underlying_symbol is not None:
        url = url+ 'variety/'

        if underlying_symbol == 'cu':
            url = url+'SHFEOPTION/1'
            params.update(_='1673580273083')

        elif underlying_symbol == 'ru':
            url = url+'SHFEOPTION/2'
            params.update(_='1673580273136')

        elif underlying_symbol == 'au':
            url = url+'151/3'
            params.update(_='1673580273148')

        elif underlying_symbol == 'al':
            url = url+'151/4'
            params.update(_='1673580273155')

        elif underlying_symbol == 'zn':
            url = url+'151/5'
            params.update(_='1673580273159')

        elif underlying_symbol == 'rb':
            url = url+'151/6'
            params.update(_='1673580273162')

        elif underlying_symbol == 'ag':
            url = url+'151/7'
            params.update(_='1673580273168')

        # dce_underlying_symbols = ['m', 'c', 'i', 'pg', 'pp', 'v', 'l', 'p', 'a', 'b', 'y']
        elif underlying_symbol == 'm':
            url = url+'DCEOPTION/1'
            params.update(_ = '1673587179838')

        elif underlying_symbol == 'c':
            url = url+'DCEOPTION/2'
            params.update(_ = '1673587179838')

        elif underlying_symbol == 'm':
            url = url+'DCEOPTION/1'
            params.update(_ = '1673587179838')
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
    """
    东方财富网-行情中心-期权市场
    https://quote.eastmoney.com/center
    :param underlying_code:
    :param exchange_name: 'she', ''
    :return: optin information given underlying code or exchange name, if neither of them are given, return all current trading options
    :rtype: panda.DataFrame
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

    #could use else instead of elif, and add raise exception in conditional else
    elif underlying_code is None and exchange_name is not None:
        if exchange_name == 'ccfex':
            return get_ccfex_option()

        elif exchange_name == 'sse':
            params.update(cb='jQuery1124010207212922928854_1673574036024', fs='m:10', _='1673574036025')

        elif exchange_name == 'szse':
            params.update(cb='jQuery1124010207212922928854_1673574036020', fs='m:12', _='1673574036037')

        elif exchange_name in ['shfe', 'dce', 'czce', 'ine']:
            return get_commodity_option(exchange_name = exchange_name)

        else:
            raise Exception('Wrong Exchange Name Input!')

    elif underlying_code is not None and exchange_name is None:
        # equity
        if underlying_code == '510050':
            params.update(cb='jQuery1124010207212922928854_1673574036020', fs='m:10+c:510050', _='1673574036045')

        elif underlying_code == '510300':
            params.update(cb='jQuery1124010207212922928854_1673574036024', fs='m:10+c:510300', _='1673574036065')

        elif underlying_code == '510500':
            params.update(cb='jQuery1124010207212922928854_1673574036024', fs='m:10+c:510500', _='1673574036100')

        elif underlying_code == '159919':
            params.update(cb='jQuery1124010207212922928854_1673574036024', fs='m:12+c:159919', _='1673574036148')

        elif underlying_code == '159922':
            params.update(cb='jQuery1124010207212922928854_1673574036024', fs='m:12+c:159922', _='1673574036157')

        elif underlying_code == '159915':
            params.update(cb='jQuery1124010207212922928854_1673574036024', fs='m:12+c:159915', _='1673574036176')

        elif underlying_code == '000300' or '000016' or '000852':
            return get_ccfex_option(underlying_code)

        # commodity


        else:
            raise Exception('Wrong Underlying Code Input!')

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
    shfe_underlying_symbols = ['cu','ru','au','al','zn','rb','ag']
    dce_underlying_symbols = ['m', 'c', 'i', 'pg', 'pp', 'v', 'l', 'p', 'a', 'b', 'y']
    exchange_strs = ['shfe', 'dce', 'czce', 'ine']
    test_df = get_commodity_option(underlying_symbol = 'c')
    print(test_df)
    # for shfe_underlying_symbol in shfe_underlying_symbols:
    #     test_df = get_commodity_option(underlying_symbol=shfe_underlying_symbol)
    #     test_df.to_csv(shfe_underlying_symbol + '_test_df.csv')
    # for exchange in exchange_strs:
    #     test_df = get_current_option(exchange_name=exchange)
    #     print(test_df)

