import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)
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
import mns_common.component.em.em_stock_info_api as em_stock_info_api

mongodb_util = MongodbUtil('27017')
mongodbUtilV2_27019 = MongodbUtilV2('27019', extra_income_db_name.EXTRA_INCOME)


def upload_etf_to_baidu():
    a_stock_path = '/A股/ETF/'

    now_date_time = datetime.now()
    now_year = now_date_time.year
    month = now_date_time.month
    a_stock_path = a_stock_path + str(now_year) + '/' + str(month)
    # 创建路径
    baidu_yun_pan_handle_service.mkdir_baidu_new_folder(a_stock_path)
    em_a_etf_info_df = em_stock_info_api.get_etf_info()

    em_a_etf_info_df = classify_symbol(em_a_etf_info_df)

    em_a_etf_info_df['symbol'] = em_a_etf_info_df.apply(
        lambda row: row['symbol'] + '.SZ' if row['classification'] in ['S', 'C']
        else row['symbol'] + '.BJ' if row['classification'] in ['X']
        else row['symbol'] + '.SH',
        axis=1
    )

    file_folder_df = baidu_yun_pan_handle_service.get_file_folder(a_stock_path)
    if data_frame_util.is_not_empty(file_folder_df):
        # 去除文件名中的 .csv 后缀
        file_folder_df['name'] = file_folder_df['name'].str.replace(r'\.csv$', '', regex=True)
        em_a_etf_info_df = em_a_etf_info_df.loc[~(em_a_etf_info_df['symbol'].isin(file_folder_df['name']))]
    fail_list = []
    for stock_one in em_a_etf_info_df.itertuples():
        symbol = stock_one.symbol
        name = stock_one.name
        try:

            col_name = extra_income_db_name.ONE_MINUTE_K_LINE_BFQ_ETF + '_' + str(now_year)

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


def classify_symbol(etf_real_time_quotes):
    etf_real_time_quotes['classification'] = etf_real_time_quotes['market'].apply(
        lambda market: classify_symbol_one(market))
    return etf_real_time_quotes


# 单个股票分类
def classify_symbol_one(market):
    if market == 0:
        return 'S'
    else:
        return 'H'


if __name__ == '__main__':
    upload_etf_to_baidu()
