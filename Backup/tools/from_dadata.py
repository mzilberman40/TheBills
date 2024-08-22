# https://github.com/hflabs/dadata-py
import os

from dadata import Dadata
import environ
from collections import defaultdict
from pprint import pprint

from TheBilling.settings import BASE_DIR

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

DADATA_TOKEN = env('DADATA_TOKEN')
DADATA_SECRET = env('DADATA_SECRET')


class DADATA:
    dadata = Dadata(DADATA_TOKEN, DADATA_SECRET)


class Countries(DADATA):
    """
    Название	    Описание
    value	        Значение одной строкой (как показывается в списке подсказок)
    data.code	    Цифровой код страны
    data.alfa2	    Буквенный код альфа-2
    data.alfa3	    Буквенный код альфа-3
    data.name_short	Краткое наименование страны
    data.name	    Полное официальное наименование страны

    Источник данных: Общероссийский классификатор стран мира (ОКСМ)
    """

    def find(self, s: str) -> list:
        # Поиск стран по части имени
        return self.dadata.suggest("country", query=s)

    def get_by_id(self, id: str):
        # Поиск стран по code, alfa2, alfa3
        res = self.dadata.find_by_id("country", id)
        if res:
            return res[0]


class LK(DADATA):

    def get_stat(self):
        return self.dadata.get_daily_stats()


class Address(DADATA):

    def parse_address(self, address: str) -> dict:
        return self.dadata.clean("address", address)


class Party(DADATA):
    def __init__(self, inn):
        self.inn = inn
        self._party_dict = self.find_by_inn(inn)
        self._value = self._party_dict.get('value')
        self._unrestricted_value = self._party_dict.get('unrestricted_value')
        self.data = self._party_dict.get('data') if self._party_dict else {}
        self.address_data = self.data.get('address')
        self.kpp = self.data.get('kpp')
        self.management = self.data.get('management')
        self.name = self.data.get('name')
        self.fio = self.data.get('fio', {})
        self.ogrn = self.data.get('ogrn')
        self.okato = self.data.get('okato')
        self.okogu = self.data.get('okogu')
        self.okpo = self.data.get('okpo')
        self.oktmo = self.data.get('oktmo')
        self.okved = self.data.get('okved')
        self.opf = self.data.get('opf', {})
        self.state = self.data.get('state')

    def find_by_inn(self, inn: str) -> dict:
        parties = self.dadata.find_by_id("party", inn)
        return parties[0] if parties else {}


class Bank(DADATA):
    def __init__(self, bik):
        self.bik = bik
        self._party_dict = self.find_by_bik(bik)
        self._value = self._party_dict.get('value')
        self._unrestricted_value = self._party_dict.get('unrestricted_value')
        self.data = self._party_dict.get('data') if self._party_dict else {}
        self._address_data = self.data.get('address', {})
        self.address_data = self._address_data.get('data', {})
        self.address = self._address_data.get('unrestricted_value') or self._address_data.get('value')
        self.corr_account = self.data.get('correspondent_account')
        self.inn = self.data.get('inn')
        self.kpp = self.data.get('kpp')
        self.name = self.data.get('name', {})
        self.okpo = self.data.get('okpo')
        self.opf = self.data.get('opf', {})
        self.payment_city = self.data.get('payment_city')
        self.registration_number = self.data.get('registration_number')
        self.state = self.data.get('state', {})
        self.swift = self.data.get('swift')

    def find_by_bik(self, bik: str) -> dict:
        result = self.dadata.find_by_id("bank", bik)
        return result[0] if result else {}


class Person(DADATA):
    def __init__(self, s: str):
        self.string = s
        self.cleaned_data = self.clean(s)
        self.first_name = self.cleaned_data.get('name')
        self.middle_name = self.cleaned_data.get('patronymic')
        self.last_name = self.cleaned_data.get('surname')
        self.gender = self.cleaned_data.get('gender', 'Unknown')
        self.ret_code = self.cleaned_data.get('qc')

    def clean(self, s: str) -> dict:
        return self.dadata.clean("name", s)


def dadata_country2dict(country: dict) -> dict:
    d = defaultdict(str)
    data = country.get('data')
    d['rus_name'] = country.get('value')
    if data:
        d['rus_name_official'] = data.get('name') or data.get('name_short')
        d['rus_name_short'] = data.get('name_short')
        d['iso3166'] = data.get('code')
        d['alfa2'] = data.get('alfa2')
        d['alfa3'] = data.get('alfa3')

    return d


def main():
    # c = Countries()
    # result = c.get_by_id("ukr")
    # print(result)
    # # result = c.find("Германия")
    #
    # result = c.get_by_id("de")
    # print(result)

    # lk = LK()
    # result = lk.get_stat()
    # print(result)

    # a = Address()
    # addr = "Ярославль"
    # pprint(a.parse_address(addr))

    # inn = '7606076730'
    # inn = '7604016045'
    # inn = '760200705164'
    # inn = '760417185190'  # Гречин
    # inn = '760606006897'    # Краш
    # inn = '760216378931'  # Skoryukov
    # p = Party(inn)
    # print(p._value)
    # print(p._unrestricted_value)
    # print(p._party_dict)
    #
    # pprint(p.data)
    # pprint(p)
    # print(p.inn)
    # bik = '044525174'
    # bik = '044525861'
    # bik = '290000103'
    # bik = '047888670'
    # bik = '045402740'
    bik = '044525181'

    b = Bank(bik)
    pprint(b.__dict__)
    # person = 'Скарюков Дмитрий Сергеевич'
    # person = "OOO Рога и Копыта"
    # # person = "Зильберман"
    # # person = "Зильберман Михаил Львович"
    # person = "Зильберман Елена Михайловна"
    # person = 'Silvercom.RU'
    # person = 'Michael Zilberman'
    # person = 'Stiv Jobs'
    # person = 'Anderson Michael'
    # p = Person(person)
    # print(p)
    # pprint(p.cleaned_data)
    # print(p)


if __name__ == "__main__":
    main()
