import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import mns_scheduler.extraIncome.us.one_minute.stock.down_load.rename.rename_stock as rename_stock
from loguru import logger
import time
import mns_common.utils.data_frame_util as data_frame_util
from mns_common.db.MongodbUtil import MongodbUtil
from mns_common.db.v2.MongodbUtilV2 import MongodbUtilV2
import mns_common.constant.extra_income_db_name as extra_income_db_name
import mns_scheduler.extraIncome.us.one_minute.api.alpha_vantage_api as alpha_vantage_api
import pandas as pd

mongodb_util_27017 = MongodbUtil('27017')
mongodbUtilV2_27019 = MongodbUtilV2('27019', extra_income_db_name.EXTRA_INCOME)
import threading


def handle_fail_sync():
    begin_year = 2025
    end_year = 2020
    while begin_year > end_year:
        query = {"now_year": {"$in": [begin_year, str(begin_year)]}}
        us_fail_df = mongodb_util_27017.find_query_data('us_stock_one_minute_down_load_fail', query)
        us_fail_df = us_fail_df.sort_values(by=['now_month'], ascending=False)
        fix_name_df = rename_stock.read_csv_df()
        for stock_one in us_fail_df.itertuples():
            symbol = stock_one.symbol
            now_month = stock_one.now_month
            path = stock_one.path
            fix_name_df_one = fix_name_df.loc[fix_name_df['current_code'] == symbol]
            try:

                if data_frame_util.is_not_empty(fix_name_df_one):
                    current_code = list(fix_name_df_one['current_code'])[0]
                    former_code = list(fix_name_df_one['former_code'])[0]

                    change_date = list(fix_name_df_one['change_date'])[0]

                    changed = list(fix_name_df_one['changed'])[0]
                    if changed:
                        change_month = change_date.strftime('%Y-%m')
                        if change_month == now_month:
                            df_01 = call_with_timeout(sync_one_minute_data,
                                                      current_code,
                                                      now_month,
                                                      timeout=60)
                            df_02 = call_with_timeout(sync_one_minute_data,
                                                      former_code,
                                                      now_month,
                                                      timeout=60)

                            export_original_data(df_01, current_code, str(begin_year), now_month)
                            export_original_data(df_02, former_code, str(begin_year), now_month)
                        elif change_month > now_month:
                            df_02 = call_with_timeout(sync_one_minute_data,
                                                      former_code,
                                                      now_month,
                                                      timeout=60)
                            export_original_data(df_02, former_code, str(begin_year), now_month)

                        elif change_month < now_month:
                            df_01 = call_with_timeout(sync_one_minute_data,
                                                      current_code,
                                                      now_month,
                                                      timeout=60)
                            export_original_data(df_01, current_code, str(begin_year), now_month)
                    else:
                        df = call_with_timeout(sync_one_minute_data,
                                               symbol,
                                               now_month,
                                               timeout=60)
                        export_original_data(df, symbol, str(begin_year), now_month)
                else:
                    df = call_with_timeout(sync_one_minute_data,
                                           symbol,
                                           now_month,
                                           timeout=60)
                    export_original_data(df, symbol, str(begin_year), now_month)
                remove_query = {'symbol': symbol, 'now_month': now_month}
                mongodb_util_27017.remove_data(remove_query, 'us_stock_one_minute_down_load_fail')
                logger.info("同步股票分钟数据完成:,{},{}", symbol, now_month)
            except BaseException as e:
                time.sleep(1)
                fail_dict = {
                    '_id': symbol + '_' + now_month,
                    'type': "stock",
                    'path': path,
                    'symbol': symbol,
                    'now_year': begin_year,
                    'now_month': now_month,
                }
                fail_df = pd.DataFrame(fail_dict, index=[1])

                mongodb_util_27017.save_mongo(fail_df, 'us_stock_one_minute_down_load_fail')
                logger.error("同步股票分钟数据出现异常:,{},{},{}", e, symbol, now_month)

        begin_year = begin_year - 1


def export_original_data(df, symbol, year, now_month):
    path = r'F:\us_stock\one_minute\{}'.format(year)
    if not os.path.exists(path):
        os.makedirs(path)

    path = path + '\{}'.format(now_month)
    if not os.path.exists(path):
        os.makedirs(path)

    file_name = path + '\{}.csv'.format(symbol)
    if data_frame_util.is_not_empty(df):
        # df = df.dropna(subset=['_id'])
        # del df['str_day']
        # del df['minute']
        # del df['_id']
        # del df['symbol']
        df.to_csv(file_name, index=False, encoding='utf-8')


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


if __name__ == '__main__':
    handle_fail_sync()
