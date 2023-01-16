import requests
import pandas as pd
import json
def index_zh_a_hist(
    symbol: str = "000859",
    period: str = "daily",
    start_date: str = "19700101",
    end_date: str = "22220101",
) -> pd.DataFrame:
    """
    东方财富网-中国股票指数-行情数据
    http://quote.eastmoney.com/concept/sh603777.html?from=classic
    :param symbol: 指数代码
    :type symbol: str
    :param period: choice of {'daily', 'weekly', 'monthly'}
    :type period: str
    :param start_date: 开始日期
    :type start_date: str
    :param end_date: 结束日期
    :type end_date: str
    :return: 行情数据
    :rtype: pandas.DataFrame
    """
    code_id_dict = index_code_id_map_em()
    period_dict = {"daily": "101", "weekly": "102", "monthly": "103"}
    url = "http://push2his.eastmoney.com/api/qt/stock/kline/get"
    try:
        params = {
            "secid": f"{code_id_dict[symbol]}.{symbol}",
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": period_dict[period],
            "fqt": "0",
            "beg": "0",
            "end": "20500000",
            "_": "1623766962675",
        }
    except KeyError:
        params = {
            "secid": f"1.{symbol}",
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": period_dict[period],
            "fqt": "0",
            "beg": "0",
            "end": "20500000",
            "_": "1623766962675",
        }
        r = requests.get(url, params=params)
        data_json = r.json()
        if data_json["data"] is None:
            params = {
                "secid": f"0.{symbol}",
                "ut": "7eea3edcaed734bea9cbfc24409ed989",
                "fields1": "f1,f2,f3,f4,f5,f6",
                "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
                "klt": period_dict[period],
                "fqt": "0",
                "beg": "0",
                "end": "20500000",
                "_": "1623766962675",
            }
            r = requests.get(url, params=params)
            data_json = r.json()
            if data_json["data"] is None:
                params = {
                    "secid": f"2.{symbol}",
                    "ut": "7eea3edcaed734bea9cbfc24409ed989",
                    "fields1": "f1,f2,f3,f4,f5,f6",
                    "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
                    "klt": period_dict[period],
                    "fqt": "0",
                    "beg": "0",
                    "end": "20500000",
                    "_": "1623766962675",
                }
    r = requests.get(url, params=params)
    data_json = r.json()
    try:
        temp_df = pd.DataFrame(
            [item.split(",") for item in data_json["data"]["klines"]]
        )
    except:
        # 兼容 000859(中证国企一路一带) 和 000861(中证央企创新)
        params = {
            "secid": f"2.{symbol}",
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "fields1": "f1,f2,f3,f4,f5,f6",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61",
            "klt": period_dict[period],
            "fqt": "0",
            "beg": "0",
            "end": "20500000",
            "_": "1623766962675",
        }
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


def get_current_index(index_symbol = None):
    pass