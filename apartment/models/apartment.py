from apartment.models.api import BienMaVilleAPIRead
from apartment.models.shared import Model

# id_zone;INSEE;LIBGEO;DEP;REG;EPCI;TYPPRED;loypredm2;lwr.IPm2;upr.IPm2;R2adj;NBobs_maille;NBobs_commune


class ApartmentInput(Model):
    department: str
    surface: int
    max_rent: float


class ApartmentInformationView(Model):
    def set_city_rating(self, list_of_city: list[BienMaVilleAPIRead]):
        """
        It takes a list of objects of type BienMaVilleAPIRead and sets the city_rating attribute of the object on which the
        function is called to the grade attribute of the object in the list that has the same name attribute

        :param list_of_city: list[BienMaVilleAPIRead]
        :type list_of_city: list[BienMaVilleAPIRead]
        """
        for city in list_of_city:
            if city.name == self.name:
                self.city_rating = city.grade

    name: str
    zip_code: str
    population: int | None
    average_rent: float
    city_rating: float | None
