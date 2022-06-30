from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

url = 'postgresql://postgres:1873@localhost:5000/hrms'

engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db_session = SessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
