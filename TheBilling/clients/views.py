from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    print(request)
    return HttpResponse(f"The clients of the Billing ))")
