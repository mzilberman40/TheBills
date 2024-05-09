from django.urls import path
# from . import views
import handbooks.views as hview

app_name = "handbooks"

urlpatterns = [
    path('currencies/', hview.show_currencies, name="currencies"),

    path('legal_forms/', hview.LegalFormsList.as_view(), name='legal_forms_list_url'),
    path('legal_form/create/', hview.LegalFormCreate.as_view(), name='legal_form_create_url'),
    path('legal_form/<int:pk>/', hview.LegalFormDetails.as_view(), name='legal_form_details_url'),
    path('legal_form/<int:pk>/update/', hview.LegalFormUpdate.as_view(), name='legal_form_update_url'),
    path('legal_form/<int:pk>/delete/', hview.LegalFormDelete.as_view(), name='legal_form_delete_url'),

    path('countries/', hview.CountriesList.as_view(), name='countries_list_url'),
    path('countries/create/', hview.CountryCreate.as_view(), name='country_create_url'),
    path('countries/<int:pk>/', hview.CountryDetails.as_view(), name='country_details_url'),
    path('countries/<int:pk>/update/', hview.CountryUpdate.as_view(), name='country_update_url'),
    path('countries/<int:pk>/delete/', hview.CountryDelete.as_view(), name='country_delete_url'),
]
