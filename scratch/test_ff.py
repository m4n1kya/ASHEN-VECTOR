import pandas_datareader.data as web
import datetime

start = datetime.datetime(2020, 1, 1)
try:
    df = web.DataReader('F-F_Research_Data_5_Factors_2x3_daily', 'famafrench', start=start)
    print(df[0].tail())
except Exception as e:
    print(f"Error: {e}")
