from fastapi import APIRouter, Depends

from apartment.controllers.apartment import ApartmentController
from apartment.dependencies import get_apartment_controller
from apartment.models.apartment import ApartmentInformationView, ApartmentInput

router = APIRouter(
    prefix="/apartment",
    tags=["apartment"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[ApartmentInformationView])
async def get_most_profitable_city(
    *,
    user_preferences: ApartmentInput = Depends(),
    apartment_controller: ApartmentController = Depends(
        get_apartment_controller
    ),
) -> list[ApartmentInformationView] | None:
    """
    > Given a user's preferences, return the most profitable city to invest in
    """
    return apartment_controller.get_most_profitable_city(user_preferences)
