# import boto3
import pandas as pd
import requests
from datetime import timedelta, date
import json
import databases
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.sql import text



def uploadtoS3(asset_name,df):
    
    type = 'emission'
    DATABASE_URL = "postgresql://postgres:Mypassword135*@3.64.136.140:5432/postgres"

    database = databases.Database(DATABASE_URL)

    metadata = sqlalchemy.MetaData()

    sqlalchemy.Table(
        asset_name+type,
        metadata,
        sqlalchemy.Column("Date", sqlalchemy.String),
        sqlalchemy.Column("Energy Consumption", sqlalchemy.Float),
        sqlalchemy.Column("Carbon Emission", sqlalchemy.Float)
    )

    engine = sqlalchemy.create_engine(
        DATABASE_URL
    )
    metadata.create_all(engine)

    # ----------------------------Conversion Formula------------------------------------------------------------    
    
    df['conv_factor'] = '0.2556'
    df["Energy Consumption"] = pd.to_numeric(df["Energy Consumption"], downcast="float")
    df["conv_factor"] = pd.to_numeric(df["conv_factor"], downcast="float")
    df["Carbon Emission"] = df["Energy Consumption"] * df["conv_factor"]
    df.drop(['conv_factor'] , inplace=True, axis=1)
    df.to_sql(asset_name+type, con=engine, if_exists='append', index=False)
    # emission = Table(asset_name+type, metadata, autoload=True)

    # DBSession = sessionmaker(bind=engine)

    # session = DBSession()

    # results = session.query(emission)

    # data = results.all()
    
    # li = []
    # for c in data:
    #     li.append({"Date": c[0], "Energy Consumption": c[1],
    #                "Carbon Emission": c[2]})

    # return (li)              

    return {"assetName": asset_name}

    # json_data = df.to_dict('records')
    # return json_data

