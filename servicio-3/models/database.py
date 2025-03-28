from databases import Database
from sqlalchemy import create_engine, MetaData

DATABASE_URL = "mysql+pymysql://admin:admin@mysql/pruebadbsql"

engine = create_engine(DATABASE_URL)

database = Database(DATABASE_URL)
metadata = MetaData()
