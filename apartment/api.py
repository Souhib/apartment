from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import NoResultFound
from starlette.responses import JSONResponse

from apartment.routers.apartment import router as apartment_router


def create_app() -> FastAPI:
    """
    It creates a FastAPI app, adds CORS middleware, and includes the routers we created earlier
    :return: A FastAPI object
    """
    origins = ["*"]
    app = FastAPI(title="Appartement")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(apartment_router)

    @app.exception_handler(NoResultFound)
    async def unicorn_exception_handler(request: Request, exc: NoResultFound):
        return JSONResponse(
            status_code=404,
            content={"message": "Couldn't find requested resource"},
        )

    return app
