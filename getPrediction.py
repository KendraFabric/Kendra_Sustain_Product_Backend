import sqlalchemy.orm as _orm 
from sqlalchemy.orm import sessionmaker
import databases
import sqlalchemy
from sqlalchemy import create_engine, Table, MetaData

from prediction import prediction
# import database as _database, models as _models , schemas as _schemas

def getPrediction(name):
    engine=create_engine('postgresql://postgres:Mypassword135*@3.64.136.140:5432/postgres')
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
    engine=create_engine('postgresql://postgres:Mypassword135*@3.64.136.140:5432/postgres')
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
    engine=create_engine('postgresql://postgres:Mypassword135*@3.64.136.140:5432/postgres')
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

def getSector():
    engine=create_engine('postgresql://postgres:Mypassword135*@3.64.136.140:5432/postgres', pool_pre_ping=True)
    connection = engine.connect()
    text = "select distinct(sector) from public.emission_factors order by sector;"
    result = connection.execute(text)
    data = result.all()
    li = []
    for c in data:
        li.append(c[0])
    return (li)

def getRegion():
    engine=create_engine('postgresql://postgres:Mypassword135*@3.64.136.140:5432/postgres', pool_pre_ping=True)
    connection = engine.connect()
    text = "select distinct(region) from public.emission_factors order by region;"
    result = connection.execute(text)
    data = result.all()
    li = []
    for c in data:
        li.append(c[0])
    return (li)

def getScope():
    engine=create_engine('postgresql://postgres:Mypassword135*@3.64.136.140:5432/postgres', pool_pre_ping=True)
    connection = engine.connect()
    text = "select distinct(scope) from public.emission_factors order by scope;"
    result = connection.execute(text)
    data = result.all()
    li = []
    for c in data:
        li.append(c[0])
    return (li)

def getyearReleased():
    engine=create_engine('postgresql://postgres:Mypassword135*@3.64.136.140:5432/postgres', pool_pre_ping=True)
    connection = engine.connect()
    text = "select distinct(year_released) from public.emission_factors order by year_released;"
    result = connection.execute(text)
    data = result.all()
    li = []
    for c in data:
        li.append(c[0])
    return (li)

def getSource():
    engine=create_engine('postgresql://postgres:Mypassword135*@3.64.136.140:5432/postgres', pool_pre_ping=True)
    connection = engine.connect()
    text = "select distinct(source) from public.emission_factors order by source;"
    result = connection.execute(text)
    data = result.all()
    li = []
    for c in data:
        li.append(c[0])
    return (li)

def getEmissionFactors(sector,year_released,region,scope):
    engine=create_engine('postgresql://postgres:Mypassword135*@3.64.136.140:5432/postgres', pool_pre_ping=True)
    connection = engine.connect()
    text = "SELECT * FROM public.emission_factors where sector='{0}' and year_released='{1}' and region='{2}' and scope='{3}'".format(sector,year_released,region,scope)
    # text = "select distinct(sector) from public.emission_factors order by sector;"
    # print(text)
    result = connection.execute(text)
    data = result.all()
    li = []
    for c in data:
        li.append({"sector": c[0], "category": c[1], "name": c[2], "activity_unit": c[3], "emission_factor": {"kgCO2e-AR4": c[4],"kgCO2e-AR5": c[5]},"scope": c[10], "source": c[11], "year_released": c[12], "year_valid": c[13], "year_calculated_from": c[14], "region": c[15]})
    
    return(li)


    

    
    

    

    
    


    # print(name)
