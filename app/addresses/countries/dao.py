from app.addresses.countries.models import Country
from app.dao.base import BaseDAO


class CountryDAO(BaseDAO):
    model = Country
