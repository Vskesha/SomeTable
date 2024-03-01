import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.db_connection import get_db
from src.routes import rows
from src.schemas.schemas import MessageResponse

app = FastAPI()


@app.get("/", response_model=MessageResponse)
async def read_root() -> dict:
    """
    Returns the root of the API. It is the entry point for the application.
    :return: dict
    """
    return {"message": "This is API for working with table rows"}


@app.get("/api/db_healthchecker", response_model=MessageResponse)
async def healthchecker(db: Session = Depends(get_db)):
    """
    The db_healthchecker function is a simple function that checks the connection to the database.
    It does this by making a request to the database and checking if it returns any results.
    If there are no results, then we know something is wrong with our connection to the database.

    :param db: Session: Pass the database session to the function
    :return: A json object with a message
    """
    try:
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(
                status_code=500, detail="Database is not configured correctly"
            )
        return {"message": "Database is configured and working correctly"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error connecting to the database",
        )


app.include_router(rows.router, prefix='/api')


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
