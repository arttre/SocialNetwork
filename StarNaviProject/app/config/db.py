from dotenv import load_dotenv, find_dotenv

import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy_utils import create_database, database_exists


load_dotenv(find_dotenv())

SQLALCHEMY_DATABASE_URL = 'mysql://{0}:{1}@{2}/{3}'.format(os.environ['SQL_LOGIN'], os.environ['MYSQL_ROOT_PASSWORD'],
                                                           os.environ['SQL_HOST'], os.environ['SQL_DBNAME'])

if not database_exists(SQLALCHEMY_DATABASE_URL):
    create_database(SQLALCHEMY_DATABASE_URL)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close_all()
