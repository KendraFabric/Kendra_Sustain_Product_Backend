import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm 

DATABASE_URL = "postgresql://postgres:Mypassword135*@3.64.136.140:5432/postgres"

engine = _sql.create_engine(DATABASE_URL)

SessionLocal = _orm.sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = _declarative.declarative_base()