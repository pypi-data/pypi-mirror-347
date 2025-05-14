import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)
from loguru import logger
from mns_common.db.MongodbUtil import MongodbUtil
from mns_common.db.v2.MongodbUtilV2 import MongodbUtilV2
import mns_scheduler.extraIncome.a_stock.one_minute.common.db_create_index as db_create_index
import mns_common.constant.extra_income_db_name as extra_income_db_name
import mns_scheduler.extraIncome.us.one_minute.api.stock_etf_info_api as stock_etf_info_api
import mns_scheduler.extraIncome.us.one_minute.api.y_finance_api as y_finance_api

from datetime import datetime, timedelta

mongodb_util_27017 = MongodbUtil('27017')
mongodbUtilV2_27019 = MongodbUtilV2('27019', extra_income_db_name.EXTRA_INCOME)


def sync_us_etf_one_minute():
    us_stock_df = stock_etf_info_api.get_us_etf_info()

    # 获取当前日期
    current_date = datetime.now()
    year = current_date.year
    col_name = extra_income_db_name.US_ETF_MINUTE_K_LINE_BFQ + "_" + str(year)

    # 创建索引
    db_create_index.create_index(mongodbUtilV2_27019, col_name)

    str_day = current_date.strftime('%Y-%m-%d')
    # 计算七天前的日期 todo 修改时间
    seven_days_ago = current_date - timedelta(days=8)

    str_seven_days_ago = seven_days_ago.strftime('%Y-%m-%d')

    for stock_one in us_stock_df.itertuples():
        symbol = stock_one.symbol
        name = stock_one.name
        try:
            us_one_minute_df = y_finance_api.get_us_one_minute(symbol, str_seven_days_ago, str_day, )
            us_one_minute_df['_id'] = symbol + '_' + us_one_minute_df['time']
            mongodbUtilV2_27019.insert_mongo(us_one_minute_df, col_name)
            logger.info("同步美国ETF分钟数据完成:{},{}", symbol, name)
        except BaseException as e:
            logger.error("同步美国股票ETF数据出现异常:{},{},{}", symbol, name, e)


if __name__ == '__main__':
    sync_us_etf_one_minute()
