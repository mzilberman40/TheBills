from django.urls import path
# from . import views
import handbooks.views as hview

app_name = "handbooks"

urlpatterns = [
    # path('currencies/', hview.show_currencies, name="currencies"),

    path('currencies/', hview.CurrenciesList.as_view(), name='currencies_list_url_name'),
    path('currencies/create/', hview.CurrencyCreate.as_view(), name='currency_create_url_name'),
    path('currencies/<int:pk>/', hview.CurrencyDetails.as_view(), name='currency_details_url_name'),
    path('currencies/<int:pk>/delete/', hview.CurrencyDelete.as_view(), name='currency_delete_url_name'),

    path('legal_forms/', hview.LegalFormsList.as_view(), name='legal_forms_list_url_name'),
    path('legal_form/create/', hview.LegalFormCreate.as_view(), name='legal_form_create_url_name'),
    path('legal_form/<int:pk>/', hview.LegalFormDetails.as_view(), name='legal_form_details_url_name'),
    path('legal_form/<int:pk>/update/', hview.LegalFormUpdate.as_view(), name='legal_form_update_url_name'),
    path('legal_form/<int:pk>/delete/', hview.LegalFormDelete.as_view(), name='legal_form_delete_url_name'),

    path('countries/', hview.CountriesList.as_view(), name='countries_list_url_name'),
    path('countries/create/', hview.CountryCreate.as_view(), name='country_create_url_name'),
    path('countries/<int:pk>/', hview.CountryDetails.as_view(), name='country_details_url_name'),
    path('countries/<int:pk>/delete/', hview.CountryDelete.as_view(), name='country_delete_url_name'),

    path('res_groups/', hview.ResourceGroupList.as_view(), name='res_group_list_url_name'),
    path('res_groups/create/', hview.ResourceGroupCreate.as_view(), name='res_group_create_url_name'),
    path('res_groups/<int:pk>/', hview.ResourceGroupDetails.as_view(), name='res_group_details_url_name'),
    path('res_groups/<int:pk>/update/', hview.ResourceGroupUpdate.as_view(), name='res_group_update_url_name'),
    path('res_groups/<int:pk>/delete/', hview.ResourceGroupDelete.as_view(), name='res_group_delete_url_name'),

    path('resources/', hview.ResourceTypeList.as_view(), name='resource_type_list_url_name'),
    path('resources/create/', hview.ResourceTypeCreate.as_view(), name='resource_type_create_url_name'),
    path('resources/<int:pk>/update/', hview.ResourceTypeUpdate.as_view(), name='resource_type_update_url_name'),
    path('resources/<int:pk>/delete/', hview.ResourceTypeDelete.as_view(), name='resource_type_delete_url_name'),
    path('resources/<int:pk>/', hview.ResourceTypeDetails.as_view(), name='resource_type_details_url_name'),
]
