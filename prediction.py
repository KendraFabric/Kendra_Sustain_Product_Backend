import numpy as np 
import pandas as pd 
# import seaborn as sns
from datetime import date, timedelta
import matplotlib.pyplot as plt
import xgboost as xgb
import os
from io import BytesIO
import json
import pandas as pd
import requests
from datetime import timedelta, date
import json
import databases
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, MetaData
# from xgboost import plot_importance, plot_tree
# from sklearn.metrics import mean_squared_error, mean_absolute_error
# from datetime import datetime
plt.style.use('fivethirtyeight')

def prediction(name,data):

    type = 'prediction'
    DATABASE_URL = "postgresql://postgres:Niks1999@18.157.52.46:5432/postgres"

    database = databases.Database(DATABASE_URL)

    metadata = sqlalchemy.MetaData()

    sqlalchemy.Table(
        name+type,
        metadata,
        sqlalchemy.Column("Date", sqlalchemy.String),
        sqlalchemy.Column("Energy Prediction", sqlalchemy.Float),
        sqlalchemy.Column("Carbon Emission Prediction", sqlalchemy.Float)
    )

    engine = sqlalchemy.create_engine(
        DATABASE_URL
    )
    metadata.create_all(engine)
    # --------------------------------Conversion--------------------------------------------------------------
    # print(data)
    pjme = pd.read_csv(BytesIO(data), index_col=[0], parse_dates=[0])
    split_date = '2021-11-01'
    pjme_train = pjme.loc[pjme.index <= split_date].copy()
    pjme_test = pjme.loc[pjme.index > split_date].copy()

    def create_features(df, label=None):
        """
        Creates time series features from datetime index
        """
        df['date'] = df.index
        df['hour'] = df['date'].dt.hour
        df['dayofweek'] = df['date'].dt.dayofweek
        df['quarter'] = df['date'].dt.quarter
        df['month'] = df['date'].dt.month
        df['year'] = df['date'].dt.year
        df['dayofyear'] = df['date'].dt.dayofyear
        df['dayofmonth'] = df['date'].dt.day
        df['weekofyear'] = df['date'].dt.weekofyear
        
        X = df[['hour','dayofweek','quarter','month','year',
            'dayofyear','dayofmonth','weekofyear']]
        if label:
            y = df[label]
            return X, y
        return X

    X_train, y_train = create_features(pjme_train, label='Energy Consumption')
    X_test, y_test = create_features(pjme_test, label='Energy Consumption')

    reg = xgb.XGBRegressor(n_estimators=1000)
    reg.fit(X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            early_stopping_rounds=50, verbose=False)

    pjme_test['MW_Prediction'] = reg.predict(X_test)
    pjme_all = pd.concat([pjme_test, pjme_train], sort=False)


    today = date.today()
    d1 = today - timedelta(days=1)
    d = today + timedelta(days=30)
    date_rng = pd.date_range(start=('%s') %d1, end=('%s')%d)
    df = pd.DataFrame(date_rng, columns=['date'])
    df['volume'] = ''
    df.to_csv('predict_dataset.csv', index=False)

    test = pd.read_csv('predict_dataset.csv', index_col=[0], parse_dates=[0])
    pred_x, pred_y = create_features(test, label='volume')
    test['MW_Prediction'] = reg.predict(pred_x)
    test.drop(['volume','hour','dayofweek', 'quarter', 'month', 'year', 'dayofyear', 'dayofmonth', 'weekofyear'], axis=1, inplace=True)

    test['conv_factor'] = '0.2556'
    test["MW_Prediction"] = pd.to_numeric(test["MW_Prediction"], downcast="float")
    test["conv_factor"] = pd.to_numeric(test["conv_factor"], downcast="float")
    test["Carbon Emission"] = test["MW_Prediction"] * test["conv_factor"]
    test.drop(['conv_factor'] , inplace=True, axis=1)
    test.reset_index(drop=True, inplace=True)
    test.rename(columns={ "MW_Prediction" : "Energy Prediction", "Carbon Emission" : "Carbon Emission Prediction", "date": "Date" }, inplace = True)
    test["Energy Prediction"] = test["Energy Prediction"].astype(int)
    test["Carbon Emission Prediction"] = test["Carbon Emission Prediction"].astype(int)
    # print(test)
    
    test.to_sql(name+type, con=engine, if_exists='append', index=False)
    # emission = Table(name, metadata, autoload=True)

    # DBSession = sessionmaker(bind=engine)

    # session = DBSession()

    # results = session.query(emission)

    # data = results.all()
    
    # li = []
    # for c in data:
    #     li.append({"Date": c[0], "Energy Prediction": c[1],
    #                "Carbon Emission Prediction": c[2]})

    # return(li)
    return {"assetName": name}


    # print(test)
        # result = test.to_json(orient="table")
    # parsed = json.loads(result)
    # json.dumps(parsed, indent=4)
    # json_data = test.to_dict('records')
        #  return result
#test.to_csv('prediction.csv', index=False)
    # os.remove(os.getcwd() + r'predict_dataset.csv')
    
        