from collections import defaultdict
import tools.from_dadata as da
import tools.from_pycountry as fp
import tools.mydecorators as md
from transliterate import detect_language
from config import CCountries


DEBUG = 0


@md.tracer(DEBUG=DEBUG)
def name2country(name: str) -> dict:
    custom_countries = CCountries.find(name)
    if custom_countries:
        return custom_countries[0].to_dict()

    country = defaultdict(str)
    c = da.Countries()
    if detect_language(name) == 'ru':
        countries = c.find(name)
        if countries:
            country = da.dadata_country2dict(countries[0])
            iso3166 = country['iso3166']
            cc = fp.get_country_by_id(iso3166)
            x = fp.pycountry_country2dict(cc)
            country.update(x)
    else:
        try:
            countries = fp.find_countries(name)
        except LookupError as err:
            # print(err)
            pass
        else:
            country = fp.pycountry_country2dict(countries[0])
            iso3166 = country['iso3166']
            country.update(da.dadata_country2dict(c.get_by_id(iso3166)))
    return country
