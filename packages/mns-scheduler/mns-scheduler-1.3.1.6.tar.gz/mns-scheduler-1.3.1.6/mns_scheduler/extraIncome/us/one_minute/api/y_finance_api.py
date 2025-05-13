import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)

proxy = 'http://127.0.0.1:7890'

os.environ['HTTP_PROXY'] = proxy
os.environ['HTTPS_PROXY'] = proxy

import yfinance as yf


#
# “history”函数包含许多参数，了解它们对于正确解释您收到的数据非常重要：
#
# period：如前所述，特别有用的是值“max”。以下是有效值：1d、5d、1mo、3mo、6mo、1y、2y、5y、10y、ytd、max。
# 间隔：定义每个条形的大小。条形越小，限制越严格，只能检索 7 天的 1 分钟数据。以下是有效值：1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
# start：开始日期。服务器需要格式为 YYYY-MM-DD 的字符串。
# end：结束日期。服务器需要格式为 YYYY-MM-DD 的字符串。
# repost：定义是否包含与正常交易时间不对应的数据。默认值为 False
# auto_adjust：是否根据股票分割和股息支付调整价格。默认值是true。
# 雅虎财经获取基本数据方法
def get_us_one_minute(symbol, start_time, end_time):
    # start_time = '2025-05-01'
    # end_time = '2025-05-09'
    start_time = '2025-05-09'
    end_time = '2025-05-11'
    yf_ticker = yf.Ticker(symbol)
    df = yf_ticker.history(period='5d',
                           interval='1m',
                           start=start_time,
                           end=end_time,
                           prepost=False,
                           auto_adjust=False)
    df = df[[
        "Open",
        "High",
        "Low",
        "Close",
        "Volume",
    ]]
    df['time'] = df.index
    df.columns = [
        "open",
        "high",
        "low",
        "close",
        "volume",
        "time",
    ]
    df['time'] = df['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    # df['str_day'] = df['time'].str.slice(0, 10)
    # df['minute'] = df['time'].str.slice(11, 19)
    return df


if __name__ == '__main__':
    df=get_us_one_minute('B', '2025-05-01', '2025-05-10')
    print(df)
