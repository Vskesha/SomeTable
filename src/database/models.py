from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Row(Base):
    """Represents a row of a table in the database."""
    # you can change the name of the table
    __tablename__ = "rows"

    id = Column(Integer, primary_key=True, index=True)
    column1 = Column(String, index=True, unique=True)
    column2 = Column(Text)
    column3 = Column(Boolean)
    column4 = Column(Date)
    # you can rename columns and/or add more columns here
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
