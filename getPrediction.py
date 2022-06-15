import sqlalchemy.orm as _orm 
from sqlalchemy.orm import sessionmaker
import databases
import sqlalchemy
from sqlalchemy import create_engine, Table, MetaData

from prediction import prediction
# import database as _database, models as _models , schemas as _schemas

def getPrediction(name):
    engine=create_engine('postgresql://postgres:Niks1999@18.157.52.46:5432/postgres')
    connection = engine.connect()
    text='SELECT * FROM public."{0}"'.format(name)
    result = connection.execute(text)
    data = result.all()
    # print(data)
    li = []
    for c in data:
        li.append({"Date": c[0], "Energy Prediction": c[1],
                   "Carbon Emission Prediction": c[2]})

    return(li)

def getEmission(name):
    engine=create_engine('postgresql://postgres:Niks1999@18.157.52.46:5432/postgres')
    connection = engine.connect()
    text='SELECT * FROM public."{0}"'.format(name)
    result = connection.execute(text)
    data = result.all()
    # print(data)
    li = []
    for c in data:
        li.append({"Date": c[0], "Energy Consumption": c[1],
                   "Carbon Emission": c[2]})

    return(li)

def getEmissionFactor(year,sector,pollutant):
    engine=create_engine('postgresql://postgres:Niks1999@18.157.52.46:5432/postgres')
    connection = engine.connect()
    text="SELECT * FROM public.emissionfactor where year={0} and sector='{1}' and pollutant='{2}'".format(year,sector,pollutant)
    result = connection.execute(text)
    data = result.all()
    # print(data)
    li = []
    for c in data:
        li.append({"pollutant": c[1], "sector": c[2],
                   "source": c[3], "fuel_name": c[4], "year": c[5], "emission_factor": c[6], "unit": c[7], "activity_unit": c[8]})

    return(li)

    

    
    

    

    
    


    # print(name)
