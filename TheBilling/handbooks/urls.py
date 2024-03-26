from django.urls import path
from . import views

app_name = "handbooks"

urlpatterns = [
    path('currencies/', views.show_currencies, name="currencies"),
    ]
