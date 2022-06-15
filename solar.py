import pandas as pd
import io
import os
import requests
from datetime import datetime, timedelta, date

def solar():
    today = date.today()
    d1 = today - timedelta(days=1)
    url = 'https://api0.solar.sheffield.ac.uk/pvlive/v3?start=%sT00:00:00&end=%sT23:00:00&data_format=csv' %(d1,d1)
    s=requests.get(url).content
    df=pd.read_csv(io.StringIO(s.decode('utf-8'))) 
    for i in range(df.shape[0]): 
        if i%2 != 0:
                    df = df.drop([i], axis = 0)
                    
    result = df.to_dict('records')
    return result
