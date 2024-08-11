from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

# postgresql+psycopg: means which postgres driver to use if omitted like (postgresql://) then by default it will use psycopg2
SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# If want to connect to DB using raw queries
# for i in range(5):
#     try:
#         conn = psycopg.connect(
#             "host=localhost dbname=fastapi user=postgres password=postgres")
#         cursor = conn.cursor(row_factory=psycopg.rows.dict_row)
#         print("Connection was successful")
#         break
#     except Exception as e:
#         print(f"Error: {e}")
#         time.sleep(5)