import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)
from loguru import logger
import time
import mns_common.utils.data_frame_util as data_frame_util
from mns_common.db.MongodbUtil import MongodbUtil
from mns_common.db.v2.MongodbUtilV2 import MongodbUtilV2
import mns_common.constant.extra_income_db_name as extra_income_db_name
import mns_scheduler.extraIncome.us.one_minute.api.alpha_vantage_api as alpha_vantage_api
import pandas as pd
from pathlib import Path

mongodb_util_27017 = MongodbUtil('27017')
mongodbUtilV2_27019 = MongodbUtilV2('27019', extra_income_db_name.EXTRA_INCOME)
from datetime import datetime
import mns_scheduler.extraIncome.us.one_minute.api.stock_etf_info_api as stock_etf_info_api

import threading


# 定义一个带超时的函数调用
def call_with_timeout(func, *args, timeout=60, **kwargs):
    # 用于存储函数执行结果
    result = None
    exception = None

    # 定义一个线程目标函数
    def target():
        nonlocal result, exception
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            exception = e

    # 创建线程并启动
    thread = threading.Thread(target=target)
    thread.start()

    # 等待线程完成，最多等待 timeout 秒
    thread.join(timeout)

    # 如果线程仍然存活，说明函数超时了
    if thread.is_alive():
        raise TimeoutError(f"Function exceeded timeout of {timeout} seconds")

    # 如果函数抛出了异常，重新抛出
    if exception is not None:
        raise exception
    return result


def sync_one_minute_data(symbol, now_month):
    df = alpha_vantage_api.sync_one_minute_data(symbol, now_month)
    return df


def sync_us_stock_one_minute(now_year, now_month):
    real_time_quotes_all_us_stocks = stock_etf_info_api.get_us_stock_info()

    path = r'F:\us_stock\one_minute\{}'.format(now_year)
    if not os.path.exists(path):
        os.makedirs(path)

    path = path + '\{}'.format(now_month)
    if not os.path.exists(path):
        os.makedirs(path)
    stock_name_list = find_exist_file(path)
    real_time_quotes_all_us_stocks = real_time_quotes_all_us_stocks.loc[
        ~(real_time_quotes_all_us_stocks['symbol'].isin(stock_name_list))]
    real_time_quotes_all_us_stocks.dropna(subset=['list_date'], inplace=True)
    for stock_one in real_time_quotes_all_us_stocks.itertuples():
        flow_mv = stock_one.flow_mv
        symbol = stock_one.symbol
        try:
            symbol = stock_one.symbol
            # simple_symbol = int(stock_one.simple_symbol)
            # code = str(simple_symbol) + '.' + symbol
            list_date = str(stock_one.list_date)
            list_date_year = int(list_date[0:4])
            list_month = int(list_date[4:6])
            now_month_int = int(now_month[5:7])
            if (list_date_year > now_year) or ((list_date_year == now_year) and (list_month > now_month_int)):
                continue
            now_date = datetime.now()
            if net_work_check(now_date):
                # 休眠 6分钟
                time.sleep(5 * 60)

            df = call_with_timeout(sync_one_minute_data,
                                   symbol,
                                   now_month,
                                   timeout=60)
            df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df['str_day'] = df['time'].str.slice(0, 10)
            df['minute'] = df['time'].str.slice(11, 19)
            df['_id'] = symbol + "_" + df['time']
            df['symbol'] = symbol
            df_export_df = df.copy()
            export_original_data(df_export_df, symbol, now_year, now_month)
        except BaseException as e:
            time.sleep(1)
            fail_dict = {
                '_id': symbol + '_' + now_month,
                'type': "stock",
                'path': path,
                'symbol': symbol,
                'now_year': now_year,
                'now_month': now_month,
                'flow_mv': flow_mv,
            }
            fail_df = pd.DataFrame(fail_dict, index=[1])

            mongodb_util_27017.save_mongo(fail_df, 'us_stock_one_minute_down_load_fail')
            logger.error("同步股票分钟数据出现异常:,{},{},{}", e, symbol, now_month)
        logger.info("同步股票分钟票数据完成:{},{}", stock_one.symbol, stock_one.name)


def export_original_data(df, symbol, year, now_month):
    path = r'F:\us_stock\one_minute\{}'.format(year)
    if not os.path.exists(path):
        os.makedirs(path)

    path = path + '\{}'.format(now_month)
    if not os.path.exists(path):
        os.makedirs(path)

    file_name = path + '\{}.csv'.format(symbol)
    if data_frame_util.is_not_empty(df):
        df = df.dropna(subset=['_id'])
        del df['str_day']
        del df['minute']
        del df['_id']
        del df['symbol']
    df.to_csv(file_name, index=False, encoding='utf-8')


def net_work_check(now_date):
    hour = now_date.hour
    minute = now_date.minute
    if hour == 7 and minute == 34:
        return True
    elif hour == 9 and minute == 59:
        return True
    elif hour == 10 and minute == 29:
        return True
    elif hour == 10 and minute == 59:
        return True
    elif hour == 12 and minute == 49:
        return True
    elif hour == 13 and minute == 28:
        return True
    elif hour == 13 and minute == 58:
        return True
    elif hour == 14 and minute == 28:
        return True
    elif hour == 15 and minute == 1:
        return True
    else:
        return False


def sync_by_year(begin_year):
    begin_month = 12
    while begin_month > 0:
        if begin_month < 10:
            str_month = '0' + str(begin_month)
        else:
            str_month = str(begin_month)
        str_month = str(begin_year) + '-' + str_month
        sync_us_stock_one_minute(begin_year, str_month)
        begin_month = begin_month - 1
        logger.error("同步完成月份:{}", str_month)


def find_exist_file(folder_path):
    if not os.path.exists(folder_path):
        logger.error("错误：目录不存在:{}", folder_path)
    else:
        folder_path = Path(folder_path)
        stock_names = [f.stem for f in folder_path.glob("*.csv")]
        return stock_names


if __name__ == '__main__':
    # k_line_df = query_k_line('TSLA')
    # sync_by_year(2024)
    # sync_by_year(2022)
    # sync_by_year(2020)
    sync_by_year(2018)
    sync_by_year(2016)
    sync_by_year(2014)
    sync_by_year(2012)
    sync_by_year(2010)
    sync_by_year(2008)
    sync_by_year(2006)
    sync_by_year(2004)
    sync_by_year(2002)
    sync_by_year(2000)
