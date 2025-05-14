import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 16
project_path = file_path[0:end]
sys.path.append(project_path)
import pandas as pd


def read_csv_df():
    data = pd.read_excel(
        fr"D:\mns\mns-scheduler\mns_scheduler\extraIncome\us\one_minute\stock\down_load\rename\stock_code_changes.xlsx")
    return data


if __name__ == '__main__':
    read_csv_df()
