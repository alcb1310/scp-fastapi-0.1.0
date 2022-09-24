from fastapi import FastAPI, Depends
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, String


class settings():
    database_username = "root"
    database_password = "a1s2d3fr"
    database_hostname = "localhost"
    database_name = "scp_final"
    database_port = 3306


app = FastAPI(
    title="SCP",
    version="0.1.0",
    description="Budgeting application focused on construction companies"
)

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{settings.database_username}:{settings.database_password}" \
                          f"@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Test(Base):
    __tablename__ = "test"
    
    uuid = Column(String, primary_key=True)
    name = Column(String)
    
    class Config:
        orm_mode = True


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

try:
    connection_config_dict = {
        'user': 'root',
        'password': 'a1s2d3fr',
        'host': '127.0.0.1',
        'database': 'scp_final',
        'raise_on_warnings': True,
        'use_pure': False,
        'autocommit': False,
        'pool_size': 5
    }
    connection = mysql.connector.connect(**connection_config_dict)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
    

@app.get("/")
def home(db: Session=Depends(get_db)):
    test = db.query(Test).all()
    return test

