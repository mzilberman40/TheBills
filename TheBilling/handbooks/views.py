import moneyed
from django.shortcuts import render
import config


def show_currencies(request):
    template_name = "handbooks/currencies.html"
    currencies = [moneyed.CURRENCIES.get(c) for c in config.CURRENCIES]
    fields = ['name', 'code', 'numeric', 'countries']
    data = {
        'objects': currencies,
        'counter': len(currencies),
        'fields': fields,
        'show_query': False,
        'title': 'Currencies'
    }

    return render(request, template_name=template_name, context=data)


