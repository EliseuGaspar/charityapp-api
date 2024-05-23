from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(F"{getenv('database_uri')}")
base = declarative_base()
_session = sessionmaker(bind = engine)
session = _session()
metadata = MetaData()
metadata.reflect(bind=engine)
