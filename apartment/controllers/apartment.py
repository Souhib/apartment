import bs4
import requests
from fastapi import HTTPException
from sqlmodel import Session, select
from unidecode import unidecode

from apartment.models.apartment import ApartmentInput, ApartmentInformationView
from apartment.models.api import (
    ApartmentRentDatasetRead,
    ApartmentRentIndicator,
    GeoPoliticalAPIRead,
    BienMaVilleAPIRead,
)
from apartment.models.errors import NoResultScrapping


class ApartmentController:
    def __init__(
        self,
        session: Session,
        bien_dans_ma_ville_api_url: str,
        gov_api_geo_url: str,
    ):
        self.session = session
        self.gov_api_geo_url = gov_api_geo_url
        self.bien_dans_ma_ville_api_url = bien_dans_ma_ville_api_url

    def _get_cities_names_and_rent_by_department(
        self, user_preferences: ApartmentInput
    ) -> list[ApartmentRentDatasetRead]:
        """
        > We select the name, average rent and insee of all cities in the department of the user, where the average rent
        multiplied by the surface of the apartment is less than the maximum rent of the user, and we order the results by
        insee

        :param user_preferences: ApartmentInput
        :type user_preferences: ApartmentInput
        :return: A list of ApartmentRentDatasetRead objects
        """
        return [
            ApartmentRentDatasetRead(
                name=name, average_rent=average_rent, insee=insee
            )
            for name, average_rent, insee in self.session.exec(
                select(
                    ApartmentRentIndicator.LIBGEO,
                    ApartmentRentIndicator.loypredm2,
                    ApartmentRentIndicator.INSEE,
                )
                .where(
                    ApartmentRentIndicator.DEP == user_preferences.department
                )
                .where(
                    ApartmentRentIndicator.loypredm2 * user_preferences.surface
                    <= user_preferences.max_rent
                )
                .order_by(ApartmentRentIndicator.INSEE)
            ).all()
        ]

    def _get_cities_geographical_informations(
        self, department_code: str
    ) -> list[GeoPoliticalAPIRead]:
        """
        It fetches the cities of a given department from the French government API

        :param department_code: The department code, for example, "75" for Paris
        :type department_code: str
        :return: A list of GeoPoliticalAPIRead objects
        """
        response = requests.get(
            f"{self.gov_api_geo_url}/departements/{department_code}/communes?fields=nom,codesPostaux,population&format=json&geometry=centre"
        )
        return sorted(
            [
                GeoPoliticalAPIRead(
                    name=information["nom"],
                    zip_code=information["codesPostaux"],
                    population=information["population"],
                    insee=information["code"],
                )
                for information in response.json()
            ],
            key=lambda d: d.insee,
        )

    def _get_department_name(self, department_code: str) -> str:
        """
        It takes a department code as a string and returns the name of the department as a string

        :param department_code: The department code, e.g. "01" for Ain
        :type department_code: str
        :return: A string containing the name of the department.
        """
        return requests.get(
            f"{self.gov_api_geo_url}/departements/{department_code}?fields=nom"
        ).json()["nom"]

    def _get_number_of_pages_to_query(self, url: str) -> int:
        """
        > It takes a URL, makes a request to that URL, parses the HTML, finds the pagination element, and returns the number
        of pages to query

        :param url: The url of the page you want to scrape
        :type url: str
        :return: The number of pages to query.
        """
        pagination = bs4.BeautifulSoup(
            requests.get(url).content, "html.parser"
        ).select_one(".pagination")
        return (
            len(pagination.find_all("a", href=True)) - 1 if pagination else 1
        )

    def get_url_to_query(self, department_code: str) -> str:
        """
        It takes a department code as input and returns the URL to query the API

        :param department_code: The department code, e.g. "01" for Ain
        :type department_code: str
        :return: A string
        """
        department_name = unidecode(
            self._get_department_name(department_code).lower()
        )
        return f"{self.bien_dans_ma_ville_api_url}/classement-ville-global-{department_name}"

    def _get_cities_grades(
        self, user_preferences: ApartmentInput
    ) -> list[BienMaVilleAPIRead]:
        """
        It gets the number of pages to query, then for each page, it gets the cities and their grades, and returns them

        :param user_preferences: ApartmentInput
        :type user_preferences: ApartmentInput
        :return: A list of BienMaVilleAPIRead objects
        """
        url = self.get_url_to_query(user_preferences.department)
        number_of_pages = self._get_number_of_pages_to_query(url)
        cities_name_with_grade = []
        for page_nb in range(0, number_of_pages):
            try:
                lines = bs4.BeautifulSoup(
                    requests.get(f"{url}?page={page_nb + 1}").content,
                    "html.parser",
                ).select_one(".ville")
                cities = lines.find("tbody").find_all("tr")  # type: ignore
                for city in cities:
                    information = city.find_all("td")
                    if len(information) == 3:
                        cities_name_with_grade.append(
                            BienMaVilleAPIRead(
                                name=information[1].find("h3").string[:-5],
                                grade=float(information[2].string),
                            )
                        )
            except NoResultScrapping:
                pass
        return cities_name_with_grade

    def get_most_profitable_city(
        self, user_preferences: ApartmentInput
    ) -> list[ApartmentInformationView]:
        """
        We get the cities names and rent by department, then we get the cities geographical informations, then we get the
        cities grades, then we merge the information and set the city rating

        :param user_preferences: ApartmentInput
        :type user_preferences: ApartmentInput
        :return: A list of ApartmentInformationView
        """
        cities_name_and_rent = self._get_cities_names_and_rent_by_department(
            user_preferences
        )
        cities_geographical_information = (
            self._get_cities_geographical_informations(
                user_preferences.department
            )
        )
        cities_name_with_grade = self._get_cities_grades(user_preferences)
        merged_information = [
            ApartmentInformationView(
                **(
                    name_and_rent.dict(exclude={"insee"})
                    | geo_information.dict(exclude={"insee"})
                )
            )
            for name_and_rent, geo_information in zip(
                cities_name_and_rent, cities_geographical_information
            )
            if geo_information.insee
            in [name_and_rent.insee for name_and_rent in cities_name_and_rent]
        ]
        for apartment in merged_information:
            apartment.set_city_rating(cities_name_with_grade)
        return sorted(
            merged_information,
            key=lambda x: (x.city_rating or 0, x.population),
            reverse=True,
        )
