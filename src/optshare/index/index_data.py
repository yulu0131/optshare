import requests
import pandas as pd
import json

def get_current_index(index_symbol = None) -> pd.DataFrame:
    """ target website: https://quote.eastmoney.com/center/hszs.html 支持上证指数、深证系列指数、指数成分、以及中证系列指数

    :param index_symbol: index symbol or None
    :type index_symbol: str or None
    :returns: a row with detailed data given individual index symbol, otherwise whole data if index symbol is none
    :rtype: pandas.DataFrame
    """
    url = 'https://79.push2.eastmoney.com/api/qt/clist/get'
    params = {
        'cb': 'jQuery112405872530692912883_1673921823290',
        'pn': '1',
        'pz': '200000',
        'po': '1',
        'np': '1',
        'ut': 'bd1d9ddb04089700cf9c27f6f7426281',
        'fltt': '2',
        'invt': '2',
        'fid': 'f3',
        'fs': 'm:1+s:2,m:0+t:5,m:2',
        'fields': 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f33,f11,f62,f128,f136,f115,f152',
        '_': '1673331486214'
    }

    r = requests.get(url, params=params)
    data_text = r.text
    data_json = json.loads(data_text[data_text.find('{'):-2])
    temp_df = pd.DataFrame(data_json['data']['diff'])
    index_df = pd.DataFrame(columns=['代码',
                                     '名称',
                                     '最新价',
                                     '涨跌幅',
                                     '涨跌额',
                                     '成交量',
                                     '成交额',
                                     '振幅',
                                     '最高',
                                     '最低',
                                     '今开',
                                     '昨收',
                                     '量比'])
    index_df['代码'] = temp_df['f12']
    index_df['名称'] = temp_df['f14']
    index_df['最新价'] = pd.to_numeric(temp_df['f2'], errors='coerce')
    index_df['涨跌额'] = pd.to_numeric(temp_df['f4'], errors='coerce')
    index_df['涨跌幅'] = pd.to_numeric(temp_df['f3'], errors='coerce').astype(str) + str('%')
    index_df['成交量'] = pd.to_numeric(temp_df['f5'], errors='coerce')
    index_df['成交额'] = pd.to_numeric(temp_df['f6'], errors='coerce')
    index_df['振幅'] = pd.to_numeric(temp_df['f7'], errors='coerce')
    index_df['最高'] = pd.to_numeric(temp_df['f15'], errors='coerce')
    index_df['最低'] = pd.to_numeric(temp_df['f16'], errors='coerce')
    index_df['今开'] = pd.to_numeric(temp_df['f17'], errors='coerce')
    index_df['昨收'] = pd.to_numeric(temp_df['f18'], errors='coerce')
    index_df['量比'] = pd.to_numeric(temp_df['f10'], errors='coerce')

    if index_symbol is None:
        return index_df
    else:
        return index_df[index_df['代码'] == index_symbol]

def get_daily_index(index_symbol: str, start_date: str, end_date: str) -> pd.DataFrame:
    """ 东方财富网-中国股票指数-行情数据 https://quote.eastmoney.com/concept/sh603777.html?from=classic

    :param index_symbol: 指数代码
    :type index_symbol: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :returns: 行情数据
    :rtype: pandas.DataFrame
    """

    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    params = {
        "secid": f"1.{index_symbol}",
        "ut": "7eea3edcaed734bea9cbfc24409ed989",
        "fields1": "f1,f2,f3,f4,f5,f6",
        "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
        "klt": "101",
        "fqt": "0",
        "beg": "0",
        "end": "20500000",
        "_": "1623766962675",
    }
    r = requests.get(url, params=params)
    data_json = r.json()
    if data_json["data"] is None:
        params.update(secid=f"0.{index_symbol}")
        r = requests.get(url, params=params)
        data_json = r.json()
        if data_json["data"] is None:
            params.update(secid=f"2.{index_symbol}")

    r = requests.get(url, params=params)
    data_json = r.json()
    try:
        temp_df = pd.DataFrame(
            [item.split(",") for item in data_json["data"]["klines"]]
        )
    except:
        # 兼容 000859(中证国企一路一带) 和 000861(中证央企创新)
        params.update(secid=f"2.{index_symbol}")

        r = requests.get(url, params=params)
        data_json = r.json()
        temp_df = pd.DataFrame(
            [item.split(",") for item in data_json["data"]["klines"]]
        )

    temp_df.columns = [
        "日期",
        "开盘",
        "收盘",
        "最高",
        "最低",
        "成交量",
        "成交额",
        "振幅",
        "涨跌幅",
        "涨跌额",
        "换手率",
    ]
    temp_df.index = pd.to_datetime(temp_df["日期"])
    temp_df = temp_df[start_date:end_date]
    temp_df.reset_index(inplace=True, drop=True)
    temp_df["开盘"] = pd.to_numeric(temp_df["开盘"])
    temp_df["收盘"] = pd.to_numeric(temp_df["收盘"])
    temp_df["最高"] = pd.to_numeric(temp_df["最高"])
    temp_df["最低"] = pd.to_numeric(temp_df["最低"])
    temp_df["成交量"] = pd.to_numeric(temp_df["成交量"])
    temp_df["成交额"] = pd.to_numeric(temp_df["成交额"])
    temp_df["振幅"] = pd.to_numeric(temp_df["振幅"])
    temp_df["涨跌幅"] = pd.to_numeric(temp_df["涨跌幅"])
    temp_df["涨跌额"] = pd.to_numeric(temp_df["涨跌额"])
    temp_df["换手率"] = pd.to_numeric(temp_df["换手率"])
    return temp_df

if __name__ == "__main__":
    # test get current index
    whole_index_df = get_current_index()
    print(whole_index_df)
    test_df = get_current_index('000300')
    print(test_df)
    daily_df = get_daily_index(index_symbol='000300', start_date='19900101', end_date='20201230')
    print(daily_df)