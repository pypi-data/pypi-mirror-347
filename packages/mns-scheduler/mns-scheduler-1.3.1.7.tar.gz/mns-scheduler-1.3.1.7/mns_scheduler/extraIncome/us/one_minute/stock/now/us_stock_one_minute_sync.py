import os
import sys

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)
from loguru import logger
import mns_common.utils.data_frame_util as data_frame_util
from mns_common.db.MongodbUtil import MongodbUtil
from mns_common.db.v2.MongodbUtilV2 import MongodbUtilV2
import mns_scheduler.extraIncome.a_stock.one_minute.common.db_create_index as db_create_index
import mns_common.constant.extra_income_db_name as extra_income_db_name
import mns_scheduler.extraIncome.us.one_minute.api.stock_etf_info_api as stock_etf_info_api
import mns_scheduler.extraIncome.us.one_minute.api.y_finance_api as y_finance_api
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

mongodb_util_27017 = MongodbUtil('27017')
mongodbUtilV2_27019 = MongodbUtilV2('27019', extra_income_db_name.EXTRA_INCOME)


def sync_us_stock_one_minute():
    us_stock_df = stock_etf_info_api.get_us_stock_info()
    us_stock_df = us_stock_df.loc[us_stock_df['amount'] != 0]

    # 获取当前日期
    current_date = datetime.now()
    year = current_date.year
    col_name = extra_income_db_name.US_STOCK_MINUTE_K_LINE_BFQ + "_" + str(year)

    # 创建索引
    db_create_index.create_index(mongodbUtilV2_27019, col_name)

    str_day = current_date.strftime('%Y-%m-%d')
    # 计算七天前的日期 todo 修改时间
    seven_days_ago = current_date - timedelta(days=7)

    str_seven_days_ago = seven_days_ago.strftime('%Y-%m-%d')

    save_one_minute_data(us_stock_df, str_day, str_seven_days_ago, col_name, True)
    handle_fail_stocks()


def save_one_minute_data(us_stock_df, str_day, str_seven_days_ago, col_name, save_flag):
    col_name_status = extra_income_db_name.US_STOCK_MINUTE_K_LINE_BFQ + "_status"
    for stock_one in us_stock_df.itertuples():

        symbol = stock_one.symbol
        name = stock_one.name
        try:
            list_date = stock_one.list_date
            if mongodbUtilV2_27019.exist_data_query(col_name_status, {"str_day": str_day,
                                                                      'symbol': symbol, 'status': 'success'}):
                continue

            if not np.isnan(list_date):
                list_date = str(int(list_date))

                date_obj = datetime.strptime(list_date, '%Y%m%d')
                # 格式化为 "YYYY-MM-DD" 或其他格式
                list_date_str = date_obj.strftime('%Y-%m-%d')

                if list_date_str > str_day:
                    continue
                elif list_date_str > str_seven_days_ago:
                    str_seven_days_ago = list_date_str

            us_one_minute_df = y_finance_api.get_us_one_minute(symbol, str_seven_days_ago, str_day)
            us_one_minute_df = us_one_minute_df.fillna(0)

            us_one_minute_df['_id'] = symbol + '_' + us_one_minute_df['time']
            us_one_minute_df['symbol'] = symbol
            if save_flag:
                mongodbUtilV2_27019.insert_mongo(us_one_minute_df, col_name)
            else:
                mongodbUtilV2_27019.save_mongo(us_one_minute_df, col_name)

            result_dict = {
                '_id': symbol + "_" + str_day,
                "str_day": str_day,
                'symbol': symbol,
                'status': 'success',

            }

            result_dict_df = pd.DataFrame(result_dict, index=[1])
            mongodbUtilV2_27019.save_mongo(result_dict_df, col_name_status)
            logger.info("同步美股分钟数据完成:{},{}", symbol, name)
        except BaseException as e:
            result_dict = {
                '_id': symbol + "_" + str_day,
                "str_day": str_day,
                'symbol': symbol,
                'status': 'fail',
            }
            result_dict_df = pd.DataFrame(result_dict, index=[1])
            mongodbUtilV2_27019.save_mongo(result_dict_df, col_name_status)

            logger.error("同步美股分钟数据出现异常:{},{},{}", symbol, name, e)


def handle_fail_stocks():
    us_stock_df = stock_etf_info_api.get_us_stock_info()

    # 获取当前日期
    current_date = datetime.now()
    str_current_date = current_date.strftime('%Y-%m-%d')

    query = {'status': 'fail', 'str_day': str_current_date}
    col_name_status = extra_income_db_name.US_STOCK_MINUTE_K_LINE_BFQ + "_status"
    fail_df = mongodbUtilV2_27019.find_query_data(col_name_status, query)
    if data_frame_util.is_empty(fail_df):
        return
    else:
        fail_us_df = us_stock_df.loc[us_stock_df['symbol'].isin(fail_df['symbol'])]
        year = current_date.year
        col_name = extra_income_db_name.US_STOCK_MINUTE_K_LINE_BFQ + "_" + str(year)

        # 循环7天，每天处理一次
        for days_ago in range(7):
            try:
                # 计算当前处理日期（从今天往前推days_ago天）
                target_date = current_date - timedelta(days=days_ago)
                str_target_date = target_date.strftime('%Y-%m-%d')

                # 计算前一天日期
                previous_date = target_date - timedelta(days=1)
                str_previous_date = previous_date.strftime('%Y-%m-%d')

                # 调用保存函数
                save_one_minute_data(fail_us_df, str_target_date, str_previous_date, col_name, False)
            except BaseException as e:

                logger.error("同步美股分钟数据补偿任务出现异常:{}", e)


if __name__ == '__main__':
    sync_us_stock_one_minute()

