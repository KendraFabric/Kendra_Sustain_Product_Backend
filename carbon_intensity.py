import requests
from datetime import  timedelta, date
import json
from copy import deepcopy
import pandas as pd

def carbon_data():
    def cross_join(left, right):
        new_rows = [] if right else left
        for left_row in left:
            for right_row in right:
                temp_row = deepcopy(left_row)
                for key, value in right_row.items():
                    temp_row[key] = value
                new_rows.append(deepcopy(temp_row))
        return new_rows


    def flatten_list(data):
        for elem in data:
            if isinstance(elem, list):
                yield from flatten_list(elem)
            else:
                yield elem

    def json_to_dataframe(data_in):
        def flatten_json(data, prev_heading=''):
            if isinstance(data, dict):
                rows = [{}]
                for key, value in data.items():
                    rows = cross_join(rows, flatten_json(value, prev_heading + '.' + key))
            elif isinstance(data, list):
                rows = []
                for i in range(len(data)):
                    [rows.append(elem) for elem in flatten_list(flatten_json(data[i], prev_heading))]
            else:
                rows = [{prev_heading[1:]: data}]
            return rows

        return pd.DataFrame(flatten_json(data_in))

    today = date.today()
    d = today - timedelta(days=1)
    url = 'https://api.carbonintensity.org.uk/regional/intensity/%s/%s/regionid/13' %(d, today)
    r = requests.get(url, allow_redirects=True).content
    # json_data = r.decode('utf8').replace("'", '"')
    df = json_to_dataframe(json.loads(r))
    df.drop(['data.regionid', 'data.dnoregion', 'data.shortname', 'data.data.intensity.index'], inplace=True, axis=1)

    df.rename(columns = {'data.data.from':'From', 'data.data.to':'To', 'data.data.intensity.forecast':'Intensity','data.data.generationmix.fuel':'Fuel','data.data.generationmix.perc':'Value'}, inplace = True)
    for i in range(df.shape[0]): 
        if i%9 != 0:
            df = df.drop([i], axis = 0)
    pd.to_datetime(df['To'])
    df.drop(['Fuel', 'Value'] , inplace=True, axis=1)
    result = df.to_dict('records')
    return result
# print(df)
