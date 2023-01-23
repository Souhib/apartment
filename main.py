import uvicorn

# from dotenv import load_dotenv

# from apartment.database import create_db_and_tables, engine

from apartment.api import create_app
from apartment.database import create_tables_and_fill_from_csv, engine

app = create_app()


@app.on_event("startup")
async def startup_event():
    # load_dotenv()
    create_tables_and_fill_from_csv(engine)


@app.on_event("shutdown")
async def shutdown_event():
    engine.dispose()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9384)
