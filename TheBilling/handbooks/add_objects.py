import pycountry
from transliterate import translit, detect_language
from django.db.models import Q
from django.core.exceptions import ValidationError
from collections import defaultdict
from datetime import datetime

from handbooks.models import Country
from handbooks.forms import CountryForm
import tools.from_dadata as da
import tools.from_pycountry as fp
import tools.mydecorators as md
#
# from config import DEFAULT_COUNTRY_NAME_ENG

DEBUG = 0


@md.tracer(DEBUG=DEBUG)
def name2country(name: str) -> dict:
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


@md.tracer(DEBUG=DEBUG)
def add_country(name: str) -> Country:
    c_objs = Country.objects.filter(Q(rus_name=name) | Q(eng_name=name) | Q(rus_name_official=name)
                                    | Q(rus_name_short=name))
    if c_objs:
        return c_objs[0]

    country = name2country(name)
    # print(f"\nAddding {name}:", country, '\n')
    cf = CountryForm(country)
    if cf.is_valid():
        return cf.save()
    else:
        print(cf.errors)


def add_all_countries():
    for country in fp.get_all_countries():
        add_country(country.name)

#
# @md.tracer(DEBUG=DEBUG)
# def add_region(reg_data: dict):
#     reg_objs = []
#     reg_fias_id = reg_data.get('region_fias_id')
#     print(reg_fias_id)
#     if reg_fias_id:
#         reg_objs = Region.objects.filter(fias_id=reg_fias_id)
#         print("Reg FIASID", reg_objs)
#
#     if reg_objs:
#         return reg_objs[0]
#
#     country = reg_data.get('country') or DEFAULT_COUNTRY_NAME_ENG
#     country_obj = add_country(country)
#     name = reg_data.get('region')
#     r_type = reg_data.get('region_type_full')
#     kladr_id = reg_data.get('region_kladr_id')
#
#     reg_dict = {
#         'rus_name': name,
#         'eng_name': translit(name, 'ru', reversed=True),
#         'kladr_id': kladr_id,
#         'iso_code': reg_data.get('region_iso_code'),
#         'fias_id': reg_fias_id,
#         'country': country_obj,
#         'number': int(str(kladr_id)[:2]),
#         'type': r_type
#     }
#     # print(reg_dict)
#     rf = RegionForm(reg_dict)
#     if rf.is_valid():
#         obj = rf.save()
#         # print(obj)
#         return obj
#
#
# @md.tracer(DEBUG=DEBUG)
# def add_city(city_data: dict) -> City:
#     city_objs = []
#     city_fias_id = city_data.get('city_fias_id')
#     if city_fias_id:
#         city_objs = City.objects.filter(fias_id=city_fias_id)
#
#     if city_objs:
#         return city_objs[0]
#
#     region_data = {key: value for key, value in city_data.items() if key.startswith(('region', 'country'))}
#
#     region_obj = add_region(region_data)
#     name = city_data.get('city')
#     city_dict = {
#         'rus_name': name,
#         'eng_name': translit(name, 'ru', reversed=True),
#         'kladr_id': city_data.get('city_kladr_id'),
#         'fias_id': city_fias_id,
#         'region': region_obj
#     }
#
#     cf = CityForm(city_dict)
#     if cf.is_valid():
#         return cf.save()
#     else:
#         print(cf.errors)
#
#
# def add_currency(new_currency: pycountry.db.Data or dict):
#     """
#     If it's a new one then it's fiat or crypto currency.
#     For adding to DB you need to provide following fields:
#         'name',
#         'short_name' - alpha_3 for fiat or short name for crypto
#         'number' - iso4217 for fiat or number more then 1000 for crypto
#         all info about fiat can be found in pycountry library.
#
#     You can provide as argument:
#         pycountry.db.Data - info inserted to db directly
#         dict - for crypto as a rule. Dict have to consists all necessary fields.
#
#     """
#
#     # 1. Looking for currency in our DB
#     if isinstance(new_currency, pycountry.db.Data):
#         number = new_currency.numeric
#     elif isinstance(new_currency, dict):
#         number = new_currency.get('number')
#     else:
#         err_msg = f"""New currency {new_currency} has type {type(new_currency)}.
#                     Has to be pycountry.db.Data or dict with fields
#                     'numeric', 'name', 'short_name' """
#         raise TypeError(err_msg)
#
#     c_objs = Currency.objects.filter(number=number) if number else []
#
#     if c_objs:
#         return c_objs[0]
#
#     # 2.There is not this currency in the our DB so this is the new one and we will try to add it in our DB.
#     #
#
#     if isinstance(new_currency, pycountry.db.Data):
#         new_currency = {
#             'number': new_currency.numeric,
#             'name': new_currency.name,
#             'short_name': new_currency.alpha_3
#                     }
#     cf = CurrencyForm(new_currency)
#     if cf.is_valid():
#         return cf.save()
#
#
# def add_all_currencies():
#     for currency in fp.get_all_currencies():
#         add_currency(currency)
#
#
# @md.tracer(DEBUG=DEBUG)
# def add_bank(d_bank: dict) -> Bank:
#     """
#     d_bank is a dictionary with bank details:
#     bik, corr_account, legal_form, name, short_name, city, okato, swift, notes, country
#      where
#     bik and swift are unique
#     """
#     bik = d_bank.get('bik')
#     swift = d_bank.get('swift')
#     if bik:
#         bank_objs = Bank.objects.filter(bik=bik)
#     elif swift:
#         bank_objs = Bank.objects.filter(swift=swift)
#     else:
#         bank_objs = []
#
#     if bank_objs:
#         return bank_objs[0]
#
#     city = d_bank.get('city')
#     city_obj = add_city(city)
#     d_bank['city'] = city_obj
#
#     legal_form = d_bank.get('legal_form')
#     legal_form_objs = LegalForm.objects.filter(Q(short_name=legal_form) | Q(full_name=legal_form))
#     if legal_form_objs:
#         legal_form_obj = legal_form_objs[0]
#     else:
#         legal_form_obj = LegalForm.objects.get(short_name='UNKNOWN')
#     d_bank['legal_form'] = legal_form_obj
#     print(d_bank)
#     try:
#         bf = BankForm(d_bank)
#     except ValidationError as err:
#         print(err)
#     else:
#         if bf.is_valid():
#             return bf.save()
#         else:
#             print(bf.errors)

#
# @md.tracer(DEBUG=DEBUG)
# def add_rubank(bik: str) -> Bank or None:
#     bank_objs = Bank.objects.filter(bik=bik)
#     if bank_objs:
#         return bank_objs[0]
#
#     bank_obj = da.Bank(bik)
#     if not bank_obj.data:
#         return None
#
#     registration_date = bank_obj.state.get('registration_date')
#     if registration_date:
#         registration_date = datetime.fromtimestamp(registration_date / 1000)
#
#     liquidation_date = bank_obj.state.get('liquidation_date')
#     if liquidation_date:
#         liquidation_date = datetime.fromtimestamp(liquidation_date / 1000)
#
#     address_data = bank_obj.address_data
#     city_obj = add_city(address_data)
#
#     bank = {
#         'bik': bik,
#         'corr_account': bank_obj.corr_account,
#         'name': bank_obj.name.get('payment'),
#         'short_name': bank_obj.name.get('short') or bank_obj.name.get('payment'),
#         'city': city_obj,
#         'address': bank_obj.address,
#         'swift': bank_obj.swift,
#         'status': bank_obj.state.get('status'),
#         'registration_date': registration_date,
#         'liquidation_date': liquidation_date,
#     }
#
#     bf = BankForm(bank)
#     if bf.is_valid():
#         return bf.save()
#     else:
#         print(bf.errors)


def main():
    # country = pycountry.countries.get(alpha_2='DE')
    # print(country)
    name = 'Италия'
    c = add_country(name)
    print(c)


if __name__ == "__main__":
    main()
