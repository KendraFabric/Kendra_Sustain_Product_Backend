import fastapi as _fastapi
from typing import List
from fastapi.datastructures import UploadFile
import fastapi.security as _security
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile
import sqlalchemy.orm as _orm
import shutil
from pydantic import BaseModel
from sqlalchemy.sql.sqltypes import String
from frequency import frequency
from fuel import fuel
# from models import emissionfactor
from price import price
import services as _services, schemas as _schemas
from carbon_intensity import carbon_data
from demand import demand
from solar import solar
from transmit import transmit
from uploadtoS3 import uploadtoS3
from prediction import prediction
import json
import pandas as pd
from io import BytesIO
from starlette.responses import RedirectResponse
from getPrediction import getPrediction,getEmission,getEmissionFactor

from wind import wind
# from realtime.demand import demand

tags_metadata = [
    {
        "name": "Authentication",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Realtime API's",
        "description": "Will be same for every Authenticated User",
        
    },
    {
        "name": "Asset Register",
        "description": "Different For Different User",
        
    },
]

# class AssetNamein(BaseModel):
#     name: str

app = _fastapi.FastAPI(openapi_tags=tags_metadata,
                        title="Fintricity API",
                        version="0.0.1",)

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def main():
    return RedirectResponse(url="/docs/")

# ----------------------------------------------- Authentication ----------------------

@app.post("/api/users", tags=["Authentication"])
async def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = await _services.get_user_by_email(user.email, db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")

    user = await _services.create_user(user, db)

    return await _services.create_token(user)

@app.post("/api/token", tags=["Authentication"])
async def generate_token(
    form_data: _security.OAuth2PasswordRequestForm = _fastapi.Depends(),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    user = await _services.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid Credentials")

    return await _services.create_token(user)

@app.get("/api/users/me", response_model=_schemas.User, tags=["Authentication"])
async def get_user(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return user           

# @app.get("/api/carbon_intensity", response_model=_schemas.Intensity)
# async def get_intensity(intensity: _schemas.Intensity = _fastapi.Depends(_services.get_carbon_intensity)):
#     return intensity

# ----------------------------------------- Realtime ------------------------------------

@app.get("/api/v0.0.1/carbon_intensity", tags=["Realtime API's"])
async def get_intensity(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return carbon_data()

@app.get("/api/demand", tags=["Realtime API's"])
async def get_demand(user: _schemas.User = _fastapi.Depends(_services.get_current_user),db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return demand()

@app.get("/api/frequency", tags=["Realtime API's"])
async def get_frequency(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return frequency()

@app.get("/api/fuel", tags=["Realtime API's"])
async def get_fuel(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return fuel()

@app.get("/api/price", tags=["Realtime API's"])
async def get_price(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return price()

@app.get("/api/solar", tags=["Realtime API's"]) 
async def get_solar(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return solar()

@app.get("/api/transmit", tags=["Realtime API's"]) 
async def get_transmit(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return transmit()

@app.get("/api/wind", tags=["Realtime API's"]) 
async def get_wind(user: _schemas.User = _fastapi.Depends(_services.get_current_user)):
    return wind()

# ---------------------------------Asset Register------------------------------------

@app.post("/api/asset", tags=["Asset Register"])
async def create_asset(asset: _schemas.AssetCreate, user: _schemas.User = _fastapi.Depends(_services.get_current_user), db: _orm.Session = _fastapi.Depends(_services.get_db)):
    return await _services.create_asset(user=user, db=db, asset=asset)

@app.get("/api/asset/{owner_id}", response_model=List[_schemas.Asset], status_code=200, tags=["Asset Register"])
async def get_asset(
    owner_id: int,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return await _services.get_asset(owner_id, user, db)    

@app.delete("/api/asset/{asset_id}", status_code=204, tags=["Asset Register"])
async def delete_asset(
    asset_id: int,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.delete_asset(asset_id, user, db)
    return {"message", "Successfully Deleted"}

@app.put("/api/asset/{asset_id}", status_code=200, tags=["Asset Register"])
async def update_asset(
    asset_id: int,
    asset: _schemas.AssetCreate,
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    await _services.update_asset(asset_id, asset, user, db)
    return {"message", "Successfully Updated"}

# ---------------------------------------AssetWise data-----------------------------------------------------

@app.post("/api/emission")
async def data(assetName: str,
    # asset_name: Usernamein,
    # db: _orm.Session = _fastapi.Depends(_services.get_db),
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
    data: UploadFile = File(...), 
):
    contents = await data.read()
    df = pd.read_csv(BytesIO(contents))
    print(data.filename)
    # await _services.create_emission(df)
    # return {"message", "Successfully Updated"}
    return uploadtoS3(assetName,df)
    # print(json.dumps(contents, indent = 1))


@app.post("/api/prediction")
async def data(assetName: str,user: _schemas.User = _fastapi.Depends(_services.get_current_user),
                
                data: UploadFile = File(...)):
    contents = await data.read()
    # df = pd.read_csv(BytesIO(contents))
    return prediction(assetName,contents)


@app.get("/api/emissionfactor")
async def get_factor(
    year: int,
    sector: str,
    pollutant: str,
):
    return getEmissionFactor(year,sector,pollutant)

@app.post("/api/getPrediction")
async def get_prediction(
    name: str,
    type="prediction",
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
):
    return getPrediction(name+type)

@app.post("/api/getEmission")
async def get_emission(
    name: str,
    type="emission",
    user: _schemas.User = _fastapi.Depends(_services.get_current_user),
):
    return getEmission(name+type)




           