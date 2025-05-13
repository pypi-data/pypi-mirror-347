import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)

import csv
import requests
import pandas as pd
import mns_common.component.em.em_stock_info_api as em_stock_info_api
from functools import lru_cache


@lru_cache()
def get_us_stock_info():
    em_us_stock_info_df = em_stock_info_api.get_us_stock_info()
    em_us_stock_info_df['symbol'] = em_us_stock_info_df['symbol'].str.replace('_', '-')
    em_us_stock_info_df = em_us_stock_info_df.loc[em_us_stock_info_df['total_mv'] != 0]

    alpha_us_stock_info = get_us_stock_list()
    alpha_us_stock_info = alpha_us_stock_info.loc[alpha_us_stock_info['assetType'] == 'Stock']

    em_us_stock_info_df = em_us_stock_info_df.loc[
        em_us_stock_info_df['symbol'].isin(alpha_us_stock_info['symbol'])]
    em_us_stock_info_df = em_us_stock_info_df.sort_values(by=['flow_mv'], ascending=False)
    return em_us_stock_info_df


@lru_cache()
def get_us_etf_info():
    em_us_stock_info_df = em_stock_info_api.get_us_stock_info()
    em_us_stock_info_df['symbol'] = em_us_stock_info_df['symbol'].str.replace('_', '-')
    em_us_stock_info_df = em_us_stock_info_df.loc[em_us_stock_info_df['total_mv'] != 0]

    alpha_us_stock_info = get_us_stock_list()
    alpha_us_stock_info = alpha_us_stock_info.loc[alpha_us_stock_info['assetType'] == 'ETF']

    em_us_stock_info_df = em_us_stock_info_df.loc[
        em_us_stock_info_df['symbol'].isin(alpha_us_stock_info['symbol'])]
    em_us_stock_info_df = em_us_stock_info_df.sort_values(by=['flow_mv'], ascending=False)
    return em_us_stock_info_df


@lru_cache()
def get_us_stock_list():
    # replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key
    CSV_URL = 'https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo'
    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode('utf-8')
        cr = csv.reader(decoded_content.splitlines(), delimiter=',')
        my_list = list(cr)
        # 提取列名（第1行）
        columns = my_list[0]
        # 提取数据（第2行及以后）
        values = my_list[1:]

        # 转换为 DataFrame
        df = pd.DataFrame(values, columns=columns)
        df = df.rename(columns={'ipoDate': 'list_date'})
        return df


if __name__ == '__main__':
    get_us_stock_info()
    get_us_etf_info()
