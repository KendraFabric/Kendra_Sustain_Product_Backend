import datetime as _dt
import pydantic as _pydantic

class _UserBase(_pydantic.BaseModel):
    firstname: str
    lastname: str
    email: str
    company: str

class UserCreate(_UserBase):
    hashed_password: str

    class Config:
        orm_mode = True

class User(_UserBase):
    id: int

    class Config:
        orm_mode = True  

class _LeadBase(_pydantic.BaseModel):
    first_name: str
    last_name: str
    email: str
    company: str

class LeadCreate(_LeadBase):
    pass

class Lead(_LeadBase):
    id: int
    owner_id: int
    date_created: _dt.datetime

    class Config:
        orm_mode = True

# class _DemandBase(_pydantic.BaseModel)  :
#     Date: _dt.date
#     Time: _dt.time
#     Demand: int

# class Demand(_DemandBase):
#     pass

class _AssetBase(_pydantic.BaseModel):
    asset_name: str
    asset_type: str
    location: str

class AssetCreate(_AssetBase):
    pass

class Asset(_AssetBase):
    id : int
    owner_id: int

    class Config:
        orm_mode = True

# class _EmissionBase(_pydantic.BaseModel):
#     date: str
#     energy_consumption: float
#     carbon_emission: float

# class EmissionCreate(_EmissionBase) :
#     pass

# class Emission(_EmissionBase):
#     id : int
#     asset_id : int
    

#     class Config:
#         orm_mode = True




