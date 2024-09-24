import moneyed
from tools import custom_countries

BTC = moneyed.add_currency(
    code='BTC',
    numeric='10001',
    name='BitCoin',
    countries=['Our Galaxy (MilkyWay)', ]
)
CURRENCIES = ('BTC', 'EUR', 'GBP', 'GEL', 'ILS', 'RUB', 'TRY', 'USD', )
# CURRENCY_CHOICES = [('USD', 'USD $'), ('EUR', 'EUR €')]

CUSTOM_COUNTRIES = [
    {
        'rus_name': 'Северный Кипр',
        'rus_name_official': 'Турецкая Руспублика Северного Кипра',
        'rus_name_short': 'ТРСК',
        'iso3166': '999',
        'alfa2': 'CT',
        'alfa3': 'TNC',
        'name': 'Northern Cyprus',
        'official_name': 'Turkish Republic of Northern Cyprus (TRNC)',
        'numeric': '999',
        'status': 'Unrecognized country',

    },
]

CCountries = custom_countries.CustomCountries()
for cc in CUSTOM_COUNTRIES:
    CCountries.add_country(cc)