import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 17
project_path = file_path[0:end]
sys.path.append(project_path)
import akshare as ak

us_stock_current_df = ak.stock_us_spot()
print(us_stock_current_df)