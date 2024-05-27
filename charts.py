from highcharts_core.chart import Chart
from highcharts_core.options import Options
import pandas as pd
from io import StringIO

def preprocess(data):
    data_str=data.decode('utf-8-sig')
    data_io=StringIO(data_str)
    df=pd.read_csv(data_io)
    options=list(df.columns)
    y_opt = df.select_dtypes(include=['floating','int64'])
    # print(df.head())
    # charts=chart(df)
    return(options,df,y_opt)

