from datetime import datetime, date

from pydantic import BaseModel, Field, ConfigDict


class MessageResponse(BaseModel):
    message: str = Field(max_length=2000)


class RowModel(BaseModel):
    column1: str = Field(max_length=200)
    column2: str = Field(max_length=2000)
    column3: bool
    column4: date


class RowResponse(RowModel):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
