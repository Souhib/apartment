from typing import Generator

from functools import lru_cache

from fastapi import Depends
from sqlmodel import Session

from apartment.config import Settings
from apartment.controllers.apartment import ApartmentController

from apartment.database import engine

# I wanted to directly load the csv from the static folder
# and directly use pandas to get the information I wanted
# but after deep reflection I wanted to "show" my Database & ORM skills
# That's why I'm going to use PostgreSQL with SQLModel !

# @lru_cache()
# def get_apartment_rent_indicator() -> pd.DataFrame:
#     """
#     It reads the CSV file and returns a Pandas DataFrame
#     :return: A dataframe
#     """
#     print("READ CSV FILE")
#     df = pd.read_csv(f"{pathlib.Path().absolute()}/static/indicateurs-loyers-appartements.csv", sep=";", encoding='latin-1')
#     return df


@lru_cache()
def get_settings() -> Settings:
    """
    It returns a Settings object
    :return: Settings()
    """
    return Settings()


def get_session() -> Generator[Session, None, None]:
    """
    It creates a session, yields it, and then closes it
    """
    with Session(engine) as session:
        yield session


def get_apartment_controller(
    settings: Settings = Depends(get_settings),
    session: Session = Depends(get_session),
) -> ApartmentController:
    """
    It returns an instance of the `ApartmentController` class, which is initialized with the `bien_dans_ma_ville_api_url`
    and `gov_api_geo_url` settings, and the `get_apartment_rent_indicator` function

    :param settings: Settings = Depends(get_settings)
    :type settings: Settings
    :param apartment_rent_indicator: pd.DataFrame = Depends(get_apartment_rent_indicator)
    :type apartment_rent_indicator: pd.DataFrame
    :return: A function that returns an ApartmentController object.
    """
    return ApartmentController(
        session, settings.bien_dans_ma_ville_api_url, settings.gov_api_geo_url
    )
