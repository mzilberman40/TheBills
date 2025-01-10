from django.urls import path
# from . import views
import handbooks.views as hview
import handbooks.models as hmodels

app_name = "handbooks"

urlpatterns = [
    # path('currencies/', hview.show_currencies, name="currencies"),

    path('currencies/', hview.CurrenciesList.as_view(), name=hmodels.Currency.LOCAL_LIST_URL_NAME()),
    path('currencies/create/', hview.CurrencyCreate.as_view(), name=hmodels.Currency.LOCAL_CREATE_URL_NAME()),
    path('currencies/<int:pk>/', hview.CurrencyDetails.as_view(), name=hmodels.Currency.LOCAL_DETAILS_URL_NAME()),
    path('currencies/<int:pk>/delete/', hview.CurrencyDelete.as_view(), name=hmodels.Currency.LOCAL_DELETE_URL_NAME()),

    path('legal_forms/', hview.LegalFormsList.as_view(), name=hmodels.LegalForm.LOCAL_LIST_URL_NAME()),
    path('legal_form/create/', hview.LegalFormCreate.as_view(), name=hmodels.LegalForm.LOCAL_CREATE_URL_NAME()),
    path('legal_form/<int:pk>/', hview.LegalFormDetails.as_view(), name=hmodels.LegalForm.LOCAL_DETAILS_URL_NAME()),
    path('legal_form/<int:pk>/update/', hview.LegalFormUpdate.as_view(), name=hmodels.LegalForm.LOCAL_UPDATE_URL_NAME()),
    path('legal_form/<int:pk>/delete/', hview.LegalFormDelete.as_view(), name=hmodels.LegalForm.LOCAL_DELETE_URL_NAME()),

    path('countries/', hview.CountriesList.as_view(), name=hmodels.Country.LOCAL_LIST_URL_NAME()),
    path('countries/create/', hview.CountryCreate.as_view(), name=hmodels.Country.LOCAL_CREATE_URL_NAME()),
    path('countries/<int:pk>/', hview.CountryDetails.as_view(), name=hmodels.Country.LOCAL_DETAILS_URL_NAME()),
    path('countries/<int:pk>/delete/', hview.CountryDelete.as_view(), name=hmodels.Country.LOCAL_DELETE_URL_NAME()),

    path('res_groups/', hview.ResourceGroupList.as_view(), name=hmodels.ResourceGroup.LOCAL_LIST_URL_NAME()),
    path('res_groups/create/', hview.ResourceGroupCreate.as_view(), name=hmodels.ResourceGroup.LOCAL_CREATE_URL_NAME()),
    path('res_groups/<int:pk>/', hview.ResourceGroupDetails.as_view(), name=hmodels.ResourceGroup.LOCAL_DETAILS_URL_NAME()),
    path('res_groups/<int:pk>/update/', hview.ResourceGroupUpdate.as_view(), name=hmodels.ResourceGroup.LOCAL_UPDATE_URL_NAME()),
    path('res_groups/<int:pk>/delete/', hview.ResourceGroupDelete.as_view(), name=hmodels.ResourceGroup.LOCAL_DELETE_URL_NAME()),

    path('resources/', hview.ResourceTypeList.as_view(), name=hmodels.ResourceType.LOCAL_LIST_URL_NAME()),
    path('resources/create/', hview.ResourceTypeCreate.as_view(), name=hmodels.ResourceType.LOCAL_CREATE_URL_NAME()),
    path('resources/<int:pk>/update/', hview.ResourceTypeUpdate.as_view(), name=hmodels.ResourceType.LOCAL_UPDATE_URL_NAME()),
    path('resources/<int:pk>/delete/', hview.ResourceTypeDelete.as_view(), name=hmodels.ResourceType.LOCAL_DELETE_URL_NAME()),
    path('resources/<int:pk>/', hview.ResourceTypeDetails.as_view(), name=hmodels.ResourceType.LOCAL_DETAILS_URL_NAME()),

    path('service_names/', hview.ServiceNameList.as_view(), name=hmodels.ServiceName.LOCAL_LIST_URL_NAME()),
    path('service_names/create/', hview.ServiceNameCreate.as_view(), name=hmodels.ServiceName.LOCAL_CREATE_URL_NAME()),
    path('service_names/<int:pk>/update/', hview.ServiceNameUpdate.as_view(),
         name=hmodels.ServiceName.LOCAL_UPDATE_URL_NAME()),
    path('service_names/<int:pk>/delete/', hview.ServiceNameDelete.as_view(),
         name=hmodels.ServiceName.LOCAL_DELETE_URL_NAME()),
    path('service_names/<int:pk>/', hview.ServiceNameDetails.as_view(),
         name=hmodels.ServiceName.LOCAL_DETAILS_URL_NAME()),

]
