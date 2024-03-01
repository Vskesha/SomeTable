from fastapi import status, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.config.config import settings


DATABASE_URL = settings.database_url
engine = create_engine(DATABASE_URL)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = DBSession()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()
