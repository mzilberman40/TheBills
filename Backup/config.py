import moneyed

BTC = moneyed.add_currency(
    code='BTC',
    numeric='10001',
    name='BitCoin',
    countries=['Our Galaxy (MilkyWay)', ]
)
CURRENCIES = ('BTC', 'EUR', 'GBP', 'GEL', 'ILS', 'RUB', 'TRY', 'USD', )
# CURRENCY_CHOICES = [('USD', 'USD $'), ('EUR', 'EUR €')]