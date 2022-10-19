import typing as t
from datetime import datetime
from pydantic import BaseModel, Field


class ExternalObj(BaseModel):
    number: str = Field(...)
    name: str = Field(None)


class State(BaseModel):
    value: str = Field(...)
    date: datetime = Field(...)
    changedBy: str = Field(...)


class Note(BaseModel):
    text: str = Field(...)


class Order(BaseModel):
    number: str = Field(None)
    externalObjects: t.List[ExternalObj] = Field(..., min_items=1)
    branch: str = Field(...)
    createDate: datetime = Field(...)
    state: State = Field(None)
    note: Note = Field(None)
