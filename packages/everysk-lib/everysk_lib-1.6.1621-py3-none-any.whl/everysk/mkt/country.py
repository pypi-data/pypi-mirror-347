###############################################################################
#
# (C) Copyright 2025 EVERYSK TECHNOLOGIES
#
# This is an unpublished work containing confidential and proprietary
# information of EVERYSK TECHNOLOGIES. Disclosure, use, or reproduction
# without authorization of EVERYSK TECHNOLOGIES is prohibited.
#
###############################################################################
from everysk.config import settings
from everysk.core.http import HttpGETConnection, HttpError


class MarketDataCountry:

    ## Private attributes
    _cache: dict = {}
    _endpoint: str = 'countries'
    _primary_key: str = 'code'

    ## Public attributes
    code: str = None
    currency: str = None
    name: str = None
    region: str = None

    ## Internal methods
    def __eq__(self, value):
        cls = type(self)
        if isinstance(value, cls):
            for field in self._get_fields():
                if getattr(self, field) != getattr(value, field):
                    # If any field is different, return False
                    return False
            # If all fields are the same, return True
            return True
        # If the value is not a cls instance, return False
        return False

    def __init__(self, code: str, currency: str = None, name: str = None, region: str = None) -> None:
        self.code = code
        self.currency = currency
        self.name = name
        self.region = region

    def __ne__(self, value):
        return not self.__eq__(value)

    def __repr__(self) -> str:
        return str({field: getattr(self, field) for field in self._get_fields()})

    def __str__(self) -> str:
        return self.__repr__()

    ## Private methods
    def _get_fields(self) -> set:
        return {key for key in self.__annotations__.keys() if not key.startswith('_')}

    def _get_response(self, params: dict) -> list[dict]:
        conn = HttpGETConnection(url=self._get_url(), params=params)
        response = conn.get_response()
        result = response.json()
        if response.status_code != 200:
            raise HttpError(
                status_code=response.status_code,
                msg=f"Error fetching data from {self._get_url()} - {result.get('error') or 'Unknown error'}."
            )

        return result

    def _get_url(self) -> str:
        return f'{settings.MARKET_DATA_PUBLIC_URL}/{self._endpoint}'

    ## Public methods
    def load(self) -> None:
        value = getattr(self, self._primary_key)
        fields = self._get_fields()
        if value not in self._cache:
            params = {
                'fields': ','.join(fields),
                f'{self._primary_key}__eq': value,
            }

            response = self._get_response(params)
            if response:
                self._cache[value] = response[0]

        for field in fields:
            setattr(self, field, self._cache[value].get(field))
