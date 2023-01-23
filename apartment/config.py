from pydantic import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_name: str
    db_username: str
    db_password: str
    bien_dans_ma_ville_api_url: str
    gov_api_geo_url: str

    class Config:
        env_prefix = "APARTMENT_"
        case_sentive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
