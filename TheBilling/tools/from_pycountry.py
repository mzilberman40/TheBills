import pycountry
from collections import defaultdict


def pycountry_country2dict(country: pycountry.ExistingCountries) -> dict:
    d = defaultdict(str)
    d['eng_name_official'] = getattr(country, 'official_name', None)
    d['eng_name'] = getattr(country, 'name', None)
    d['iso3166'] = getattr(country, 'numeric', None)
    d['alfa2'] = getattr(country, 'alpha_2', None)
    d['alfa3'] = getattr(country, 'alpha_3', None)

    return d


def find_countries(name: str) -> list:
    return pycountry.countries.search_fuzzy(name)


def get_all_countries() -> list[pycountry.db.Data]:
    return list(pycountry.countries)


def get_country_by_id(id: str) -> pycountry.db.Data:
    if not isinstance(id, str):
        id = str(id)

    return pycountry.countries.get(numeric=id)


def get_currency_by_id(id: str) -> pycountry.db.Data:
    if not isinstance(id, str):
        id = str(id)
    return pycountry.countries.get(numeric=id)


def get_all_currencies() -> list[pycountry.db.Data]:
    return list(pycountry.currencies)


# def find_currencies(name: str) -> list:
#     return pycountry.currencies.search_fuzzy(name)


def main():

    # country = pycountry.countries.get(alpha_2='DE')
    # country = pycountry.countries.get(numeric='276')
    # country = pycountry.countries.search_fuzzy("land")
    # countries = list(pycountry.countries)
    # print(len(countries), countries)
    #
    # countries = list(pycountry.historic_countries)
    # print(len(countries), countries)
    # country = countries[0]
    #
    # print(country)
    # print(type(country))
    # cid = '643'
    # c = get_country_by_id(cid)
    # print(c)
    # print(pycountry_country2dict(c))
    # print(get_all_currencies())
    cur = 'dollar'
    # print(find_currencies(cur))


if __name__ == "__main__":
    main()
