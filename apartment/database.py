from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel

from apartment.config import Settings


def create_db_engine(settings: Settings) -> Engine:
    """
    It creates a database engine

    :param settings: Settings
    :type settings: Settings
    :return: An Engine object
    """
    sqlite_url = f"postgresql+psycopg2://{settings.db_username}:{settings.db_password}@{settings.db_host}/{settings.db_name}"

    return create_engine(sqlite_url, echo=True)


def create_tables_and_fill_from_csv(_engine: Engine) -> None:
    """
    > Create the database and tables.

    :param _engine: The engine that we created in the previous step
    :type _engine: Engine
    """
    SQLModel.metadata.create_all(_engine)
    # columns_to_numeric = ["id_zone", "INSEE", "DEP", "loypredm2", "lwr.IPm2", "upr.IPm2", "R2adj"]
    # df = pd.read_csv(f"{pathlib.Path().absolute()}/static/indicateurs-loyers-appartements.csv", sep=";", encoding='latin-1', decimal=",")
    # df[columns_to_numeric] = df[columns_to_numeric].apply(pd.to_numeric, errors='coerce', axis=1)
    # df.to_sql('apartmentrentindicator', con=_engine, if_exists="replace")


engine = create_db_engine(Settings())
