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

def chartvis(df,xvar,yvar,charttype):
    mychart=Chart.from_pandas(df,
                              property_map={'x':xvar,
                                            'y':yvar},
                                            # 'y':['Age 16-19','Age 20-24','Age 25-34','Age 35-44']},
                              series_type=charttype,
                              chart_kwargs = {'container': 'target_div',
                                              'variable_name': 'myChart',
                                               'credits': 'False',
                                               
  })
    
    chart=mychart.to_js_literal()
    # print(chart)
    return(chart)
