from datetime import date
from typing import List, Type, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.db_connection import get_db
from src.database.models import Row
from src.schemas.schemas import RowResponse, RowModel, MessageResponse

router = APIRouter(prefix="/rows", tags=["row"])


# Create row in a table
@router.post("/rows/",
             response_model=RowResponse,
             description='Creates one row in a table')
async def create_row(body: RowModel, db: Session = Depends(get_db)) -> Row:
    """
    Creates one row in a table from given request body
    :param body: RowModel: data to be used to create a row
    :param db: Session: database session
    :return: Row: created row
    """
    row = Row(column1=body.column1, column2=body.column2, column3=body.column3, column4=body.column4)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


# Get all rows (the whole table)
@router.get("/",
            response_model=List[RowResponse],
            description='Returns all rows in a table')
async def read_rows(skip: int = 0,
                    limit: int = 10,
                    db: Session = Depends(get_db)) -> List[Type[Row]]:
    """
    Returns all rows in a table
    :param skip: int: number of rows to skip
    :param limit: int: number of rows to return
    :param db: Session: database session
    :return: List[Row]: list of rows
    """
    return db.query(Row).offset(skip).limit(limit).all()


# Get a row by id
@router.get("/{row_id}",
            response_model=RowResponse,
            description='Returns a row by id')
async def read_row(row_id: int,
                   db: Session = Depends(get_db)) -> Type[Row]:
    """
    Returns a row by id
    :param row_id: int: id of the row
    :param db: Session: database session
    :return: Row: row with given id
    """
    row = db.query(Row).filter(Row.id == row_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Row not found")
    return row


# Update the whole row in a table
@router.put("/{row_id}",
            response_model=RowResponse,
            description='Updates whole row in table')
async def update_whole_row(row_id: int,
                           body: RowModel,
                           db: Session = Depends(get_db)) -> Type[Row]:
    """
    Updates whole row in table
    :param row_id: int: id of the row
    :param body: RowModel: data to be used to update a row
    :param db: Session: database session
    :return: Row: modified row
    """
    row = db.query(Row).filter(Row.id == row_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Row not found")

    for key, value in body.dict().items():
        setattr(row, key, value)

    db.commit()
    db.refresh(row)
    return row


# Update separate fields of a row in a table
@router.patch("/{row_id}",
              response_model=RowResponse,
              description='Updates part of row in table')
async def update_part_row(row_id: int,
                          column1: Optional[str] = None,
                          column2: Optional[str] = None,
                          column3: Optional[bool] = None,
                          column4: Optional[date] = None,
                          db: Session = Depends(get_db)) -> Type[Row]:
    """
    Updates a row in a table only with given fields
    :param row_id: int: id of the row
    :param column1: str: column1
    :param column2: str: column2
    :param column3: bool: True or False
    :param column4: date: date of column4
    :param db: Session: database session
    :return: Row: modified row
    """
    row = db.query(Row).filter(Row.id == row_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Row not found")

    if column1 is not None:
        row.column1 = column1
    if column2 is not None:
        row.column2 = column2
    if column3 is not None:
        row.column3 = column3
    if column4 is not None:
        row.column4 = column4

    db.commit()
    db.refresh(row)
    return row


# Delete a row in a table
@router.delete("/{row_id}",
               response_model=MessageResponse,
               description='Deletes a row in a table')
async def delete_row(row_id: int,
                     db: Session = Depends(get_db)) -> dict:
    """
    Deletes a row in a table
    :param row_id: int: id of the row
    :param db: Session: database session
    :return: dict: message of the operation
    """
    row = db.query(Row).filter(Row.id == row_id).first()
    if row is None:
        raise HTTPException(status_code=404, detail="Row not found")
    db.delete(row)
    db.commit()
    return {"message": f"Row with id={row_id} deleted successfully"}
