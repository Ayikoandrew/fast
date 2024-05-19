from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings 

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#dependency
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host="localhost", database="fastapi", user="ayiko", password="secret", cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("Connection to the database was successful!")
#         break
#     except Exception as e:
#         print(e)
#         time.sleep(2)