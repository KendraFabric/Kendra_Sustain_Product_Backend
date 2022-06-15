import datetime as _dt 
import sqlalchemy as _sql
import sqlalchemy.orm as _orm
import passlib.hash as _hash

import database as _database
# from schemas import Intensity

class User(_database.Base):
    __tablename__ = "users"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    firstname = _sql.Column(_sql.String)
    lastname = _sql.Column(_sql.String)
    email = _sql.Column(_sql.String, unique=True, index=True)
    company = _sql.Column(_sql.String)
    hashed_password = _sql.Column(_sql.String)

    leads = _orm.relationship("Lead", back_populates="owner")
    asset = _orm.relationship("assetRegister", back_populates="assetowner")

    def verify_password(self, password: str):
        return _hash.bcrypt.verify(password, self.hashed_password)

class Lead(_database.Base):
    __tablename__ = "leads"  
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id")) 
    first_name = _sql.Column(_sql.Integer, index=True)
    last_name = _sql.Column(_sql.Integer, index= True )
    email = _sql.Column(_sql.String, index=True)
    company = _sql.Column(_sql.String, index=True, default="") 
    date_created = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow )  

    owner = _orm.relationship("User", back_populates="leads")  

class demand(_database.Base):
    __tablename__ = "demand"
    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    Date = _sql.Column(_sql.DateTime, default=_dt.datetime.utcnow )
    Time = _sql.Column(_sql.TIME)
    Demand = _sql.Column(_sql.Integer, index=True)

class assetRegister(_database.Base):
    __tablename__ = "assetregister"
    id =  _sql.Column(_sql.Integer, primary_key=True, index=True)
    owner_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    asset_name = _sql.Column(_sql.String, index=True)
    asset_type = _sql.Column(_sql.String, index=True)
    location = _sql.Column(_sql.String, index=True)

    assetowner = _orm.relationship("User", back_populates="asset")
    # asset_owner = _orm.relationship("emissions", back_populates="emissionowner")

# class emissions(_database.Base) :
#     __tablename__ = "emission"
#     id =  _sql.Column(_sql.Integer, primary_key=True, index=True)
#     asset_id =  _sql.Column(_sql.Integer, _sql.ForeignKey("assetregister.id"))
#     date = _sql.Column(_sql.String, index=True)
#     energy_Consumption =  _sql.Column(_sql.Float, index=True)
#     carbon_Emissions = _sql.Column(_sql.Float, index=True )

#     emissionowner = _orm.relationship("assetregister", back_populates="asset_owner")

class emissionfactor(_database.Base):
    __tablename__ = "emissionfactor"
    id =  _sql.Column(_sql.Integer, primary_key=True, index=True)
    pollutant = _sql.Column(_sql.String, index=True)
    sector = _sql.Column(_sql.String, index=True)
    source = _sql.Column(_sql.String, index=True)
    fuel_name = _sql.Column(_sql.String, index=True)
    year =_sql.Column(_sql.Integer, index=True)
    emission_factor = _sql.Column(_sql.Integer, index=True)
    unit = _sql.Column(_sql.String, index=True)
    activity_units = _sql.Column(_sql.String, index=True)