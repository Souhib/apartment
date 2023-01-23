"""
Models that will be used to Read external resources such as external API
"""

import pydantic
from sqlmodel import Field

from apartment.models.shared import Model


class ApartmentRentDatasetRead(Model):
    name: str
    average_rent: float
    insee: int


class GeoPoliticalAPIRead(Model):
    name: str
    zip_code: str
    population: int
    insee: int

    @pydantic.validator("zip_code", pre=True)
    def get_zip_code(cls, v):
        if isinstance(v, list):
            return v[0]
        return v


class BienMaVilleAPIRead(Model):
    name: str
    grade: float


class CityGeographicalInformationRead(Model):
    name: str = ""
    zip_code: str = ""
    population: int = 0
    insee: int = 0

    @pydantic.validator("zip_code", pre=True)
    def get_zip_code(cls, v):
        if isinstance(v, list):
            return v[0]
        return v


class ApartmentRentIndicator(Model, table=True):
    id: int | None = Field(default=None, primary_key=True, unique=True)
    id_zone: int
    INSEE: int
    LIBGEO: str
    DEP: int
    REG: int
    EPCI: str
    TYPPRED: str
    loypredm2: float
    lwr_IPm2: float
    upr_IPm2: float
    R2adj: float
    NBobs_maille: int
    NBobs_commune: int
