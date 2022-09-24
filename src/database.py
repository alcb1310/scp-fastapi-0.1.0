from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from . import config
    
    

SQLALCHEMY_DATABASE_URL = f"mysql+mysqlconnector://{config.settings.database_username}:{config.settings.database_password}" \
                          f"@{config.settings.database_hostname}:{config.settings.database_port}/{config.settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()