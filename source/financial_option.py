import json
import requests
import pandas as pd

def current_etf_option(exchange_name) -> pd.DataFrame:
    """
    东方财富网-行情中心-期权市场
    http://quote.eastmoney.com/center
    :param exchange_name: 'she', or 'szse'
    :return: current etf option information given selected exchange name
    :rtype: pandas.DataFrame
    """

    url = 'https://36.push2.eastmoney.com/api/qt/clist/get'
    if exchange_name == "she":
        params = {
            'cb': 'jQuery112409888319082959067_1673333526884',
            'pn': '1',
            'pz': '200000',
            'po': '1',
            'np': '1',
            'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
            'fltt': '2',
            'invt': '2',
            'fid': 'f3',
            'fs': 'm:10',
            'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f28,f11,f62,f128,f136,f115,f152,f133,f108,f163,f161,f162',
            '_': '1673333526885'
        }

    elif exchange_name == "szse":
        params = {
            'cb': 'jQuery112409888319082959067_1673333526880',
            'pn': '1',
            'pz': '200000',
            'po': '1',
            'np': '1',
            'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
            'fltt': '2',
            'invt': '2',
            'fid': 'f3',
            'fs': 'm:12',
            'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f28,f11,f62,f128,f136,f115,f152,f133,f108,f163,f161,f162',
            '_': '1673333527003'
        }

    else:
        raise Exception("Error, Unsupported Exchange Name!")

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

def current_cffex_option() -> pd.DataFrame:
    """
    东方财富网-行情中心-期权市场
    http://quote.eastmoney.com/center
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



if __name__ == '__main__':
    current_she_etf = current_etf_option(exchange_name = "she")
    print(current_she_etf)
    current_szse_etf = current_etf_option(exchange_name = "szse")
    print(current_szse_etf)
    ccfex_financial_option = current_cffex_option()
    print(ccfex_financial_option)
