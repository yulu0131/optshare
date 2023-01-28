import pandas as pd
import requests

def get_bond_yield(
    start_date: str = "20200204", end_date: str = "20210124"
) -> pd.DataFrame:
    """ 中国债券信息网-国债及其他债券收益率曲线
    Warning: end_date - start date < one year

    Parameters
    ------------------
    start_date: str, 'yyyymmdd'
        start date
    end_date: str, 'yyyymmdd'
        end date

    Returns
    ------------------
    pandas.DataFrame
        Bond yield data with term structure given start date and end date
    """

    url = "https://yield.chinabond.com.cn/cbweb-pbc-web/pbc/historyQuery"
    params = {
        "startDate": '-'.join([start_date[:4], start_date[4:6], start_date[6:]]),
        "endDate": '-'.join([end_date[:4], end_date[4:6], end_date[6:]]),
        "gjqx": "0",
        "qxId": "ycqx",
        "locale": "cn_ZH",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
    }
    res = requests.get(url, params=params, headers=headers)
    data_text = res.text.replace("&nbsp", "")
    data_df = pd.read_html(data_text, header=0)[1]

    data_df['日期'] = pd.to_datetime(data_df['日期']).dt.date
    data_df['3月'] = pd.to_numeric(data_df['3月'])
    data_df['6月'] = pd.to_numeric(data_df['6月'])
    data_df['1年'] = pd.to_numeric(data_df['1年'])
    data_df['3年'] = pd.to_numeric(data_df['3年'])
    data_df['5年'] = pd.to_numeric(data_df['5年'])
    data_df['7年'] = pd.to_numeric(data_df['7年'])
    data_df['10年'] = pd.to_numeric(data_df['10年'])
    data_df['30年'] = pd.to_numeric(data_df['30年'])
    data_df.sort_values('日期', inplace=True)
    data_df.reset_index(inplace=True, drop=True)

    return data_df



if __name__ == "__main__":

    bond_china_yield_df = get_bond_yield(
        start_date="20221209", end_date="20221209"
    )
    print(bond_china_yield_df)

