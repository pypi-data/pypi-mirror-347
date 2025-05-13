import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)

from mns_common.db.MongodbUtil import MongodbUtil
from loguru import logger
import mns_scheduler.baidu.baidu_yun_pan_handle_service as baidu_yun_pan_handle_service
from mns_common.db.v2.MongodbUtilV2 import MongodbUtilV2
import mns_common.utils.data_frame_util as data_frame_util
from datetime import datetime
import mns_common.constant.extra_income_db_name as extra_income_db_name

mongodb_util = MongodbUtil('27017')
mongodbUtilV2_27019 = MongodbUtilV2('27019', extra_income_db_name.EXTRA_INCOME)

main_index_list = [
    "000001.SH",
    "000016.SH",
    "000010.SH",
    "000009.SH",
    "000015.SH",
    "399001.SZ",
    "399004.SZ",
    "399005.SZ",
    "399006.SZ",
    "000300.SH",
    "000905.SH",
    "000688.SH",
    "000903.SH",
    "000906.SH",
    "000852.SH",
    "000932.SH",
    "000933.SH",
    "980017.SZ",
    "399808.SZ",
    "399997.SZ",
]


def upload_index_to_baidu():
    a_stock_path = '/A股/主要指数/'

    now_date_time = datetime.now()
    now_year = now_date_time.year
    month = now_date_time.month
    a_stock_path = a_stock_path + str(now_year) + '/' + str(month)
    # 创建路径
    baidu_yun_pan_handle_service.mkdir_baidu_new_folder(a_stock_path)





    fail_list = []
    for symbol in main_index_list:

        try:

            col_name = extra_income_db_name.ONE_MINUTE_K_LINE_BFQ_MAIN_INDEX + '_' + str(now_year)

            if month < 10:
                month_str = '0' + str(month)
            else:
                month_str = str(month)
            begin_time = str(now_year) + '-' + month_str + '-01 09:00:00'
            query = {'symbol': symbol, 'time': {"$gte": begin_time}}
            one_minute_k_line_bfq_df = mongodbUtilV2_27019.find_query_data(col_name, query)
            if data_frame_util.is_not_empty(one_minute_k_line_bfq_df):
                one_minute_k_line_bfq_df = one_minute_k_line_bfq_df.sort_values(by=['time'], ascending=True)
                del one_minute_k_line_bfq_df['_id']
                del one_minute_k_line_bfq_df['symbol']
                result = baidu_yun_pan_handle_service.upload_to_baidu(symbol, a_stock_path, one_minute_k_line_bfq_df)
                if result != 0:
                    fail_list.append(symbol)
        except BaseException as e:
            fail_list.append(symbol)
            logger.error("上传数据异常:{}", e)




if __name__ == '__main__':
    upload_index_to_baidu()
