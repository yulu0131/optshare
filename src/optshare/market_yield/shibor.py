import requests
import json
import pandas as pd

def get_shibor(start_date: str = '20220201', end_date: str = '20230101'):
    """ target website: https://www.shibor.org/shibor/
    Warning: end_date - start date < one year

    Parameters
    -----------------
    start_date: str, 'yyyymmdd'
        start date
    end_date: str, 'yyyymmdd'
        end date

    Returns
    -----------------
    pandas.DataFrame
        shibor market_yield data with term structure given start date and end date
    """
    try:
        url = "https://www.shibor.org/ags/ms/cm-u-bk-shibor/ShiborHis"
        params = {
            'lang': 'cn',
            'startDate': '-'.join([start_date[:4], start_date[4:6], start_date[6:]]),
            'endDate': '-'.join([end_date[:4], end_date[4:6], end_date[6:]]), }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        }

        r = requests.get(url, params=params, headers=headers)
        data_text = r.text
        data_json = json.loads(data_text)
        temp_df = pd.DataFrame(data_json['records'])

        shibor_df = pd.DataFrame(columns=['日期',
                                          'O/N',
                                          '1W',
                                          '2W',
                                          '1M',
                                          '3M',
                                          '6M',
                                          '9M',
                                          '1Y'])
        shibor_df['日期'] = pd.to_datetime(temp_df['showDateCN'], errors='coerce').dt.date
        shibor_df['O/N'] = pd.to_numeric(temp_df['ON'], errors='coerce')
        shibor_df['1W'] = pd.to_numeric(temp_df['1W'], errors='coerce')
        shibor_df['2W'] = pd.to_numeric(temp_df['2W'], errors='coerce')
        shibor_df['1M'] = pd.to_numeric(temp_df['1M'], errors='coerce')
        shibor_df['3M'] = pd.to_numeric(temp_df['3M'], errors='coerce')
        shibor_df['6M'] = pd.to_numeric(temp_df['6M'], errors='coerce')
        shibor_df['9M'] = pd.to_numeric(temp_df['9M'], errors='coerce')
        shibor_df['1Y'] = pd.to_numeric(temp_df['1Y'], errors='coerce')
        shibor_df.sort_values('日期', inplace=True)
        shibor_df.reset_index(inplace=True, drop=True)

        return shibor_df

    except:
        raise Exception("Data only provided for one year or less!")


def get_lpr(start_date: str = '20220201', end_date: str = '20230101'):
    """ target website: https://www.shibor.org/shibor/
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
        LPR market_yield data with term structure given start date and end date
    """
    try:
        url = "https://www.shibor.org/ags/ms/cm-u-bk-currency/LprHis"
        params = {
            'lang': 'CN',
            'strStartDate': '-'.join([start_date[:4], start_date[4:6], start_date[6:]]),
            'strEndDate': '-'.join([end_date[:4], end_date[4:6], end_date[6:]])
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        }

        r = requests.get(url, params=params, headers=headers)
        data_text = r.text
        data_json = json.loads(data_text)
        temp_df = pd.DataFrame(data_json['records'])

        lpr_df = pd.DataFrame(columns=['日期',
                                       '1Y',
                                       '5Y'])
        lpr_df['日期'] = pd.to_datetime(temp_df['showDateCN'], errors='coerce').dt.date
        lpr_df['1Y'] = pd.to_numeric(temp_df['1Y'], errors='coerce')
        lpr_df['5Y'] = pd.to_numeric(temp_df['5Y'], errors='coerce')
        lpr_df.sort_values('日期', inplace=True)
        lpr_df.reset_index(inplace=True, drop=True)

        return lpr_df

    except:
        raise Exception("Data only provided for one year or less!")


if __name__ == '__main__':
    test_shibor_df = get_shibor()
    print(test_shibor_df)
    test_lpr_df = get_lpr()
    print(test_lpr_df)
