from pydantic import Extra
from sqlmodel import SQLModel


class Model(SQLModel):
    class Config:
        extra = Extra.forbid
