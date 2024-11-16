import moneyed


def currency_obj2dict(currency_obj):
    fields = ('name', 'code', 'numeric')
    return {field: getattr(currency_obj, field) for field in fields}


def get_all_currencies() -> list:
    return [cur.name for cur in moneyed.list_all_currencies()]


def code2currency(code):
    obj = moneyed.get_currency(code)
    data = {
        'name': obj.name,
        'code': obj.code,
        'numeric': obj.numeric,
    }
    return data
