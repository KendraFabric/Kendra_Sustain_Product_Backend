import fastapi as _fastapi
import fastapi.security as _security
import database as _database
import sqlalchemy.orm as _orm 
import jwt as _jwt
import passlib.hash as _hash
import database as _database, models as _models , schemas as _schemas
# from realtime.demand import demands
from uploadtoS3 import uploadtoS3
# from realtime.carbon import carbon
# from realtime.carbon import carbon_data

oauth2schema = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

JWT_SECRET = "myjwtsecret"

def create_database():
    # carbon_data()
    return _database.Base.metadata.create_all(bind=_database.engine)

def get_db():
    db = _database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_user_by_email(email: str,db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first() 

async def create_user(user: _schemas.UserCreate, db: _orm.Session):
    user_obj = _models.User(firstname=user.firstname, lastname=user.lastname, email=user.email,company=user.company,hashed_password=_hash.bcrypt.hash(user.hashed_password) )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

async def authenticate_user(email: str, password: str, db: _orm.Session):
    user = await get_user_by_email(db=db, email=email)

    if not user:
        return False

    if not user.verify_password(password):
        return False

    return user

async def create_token(user: _models.User):
    user_obj = _schemas.User.from_orm(user)

    token = _jwt.encode(user_obj.dict(), JWT_SECRET)

    return dict(access_token=token, token_type="bearer")

async def get_current_user(
    db: _orm.Session = _fastapi.Depends(get_db),
    token: str = _fastapi.Depends(oauth2schema),
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = db.query(_models.User).get(payload["id"])
    except:
        raise _fastapi.HTTPException(
            status_code=401, detail="Invalid Email or Password"
        )

    return _schemas.User.from_orm(user)
    

# async def get_demand(db: _orm.Session):
        
#     demands()
#     demand = db.query(_models.demand).all()

#     return demand


async def create_asset(user: _schemas.User, db: _orm.session, asset: _schemas.AssetCreate):
    asset = _models.assetRegister(**asset.dict(), owner_id=user.id)
    db.add(asset)
    db.commit()
    db.refresh(asset)
    return _schemas.Asset.from_orm(asset)

async def _asset_selector(owner_id: int, user: _schemas.User, db: _orm.Session):
    asset = (
        db.query(_models.assetRegister)
        .filter_by(owner_id=user.id)
        .filter(_models.User.id == owner_id)
        .all()
    )

    if asset is None:
        raise _fastapi.HTTPException(status_code=404, detail="Asset does not exist")

    return asset


async def get_asset(owner_id: int, user: _schemas.User, db: _orm.Session):
    asset = await _asset_selector(owner_id=owner_id, user=user, db=db)

    return list(map(_schemas.Asset.from_orm, asset))

async def delete_asset(asset_id: int, user: _schemas.User, db: _orm.Session):
    asset = (
        db.query(_models.assetRegister)
        .filter_by(owner_id=user.id)
        .filter(_models.assetRegister.id == asset_id)
        .first()
    )

    db.delete(asset)
    db.commit()

async def update_asset(asset_id: int, asset: _schemas.AssetCreate, user: _schemas.User, db: _orm.Session):
    asset_db = (
        db.query(_models.assetRegister)
        .filter_by(owner_id=user.id)
        .filter(_models.assetRegister.id == asset_id)
        .first()
    )

    asset_db.asset_name = asset.asset_name
    asset_db.asset_type = asset.asset_type
    asset_db.location = asset.location
    

    db.commit()
    db.refresh(asset_db)

    return _schemas.Asset.from_orm(asset_db)       

async def create_emission( df):
    # print(df)
    return uploadtoS3(df)

# SELECT * FROM public.emissionfactor where year=2018 and sector='Energy' and pollutant='Nitrous Oxide'; 

async def emission():
    print('Niks')

