from django.urls import path
from . import views
from .views import LegalFormsList, LegalFormCreate, LegalFormUpdate, LegalFormDelete, LegalFormDetails

app_name = "handbooks"

urlpatterns = [
    path('currencies/', views.show_currencies, name="currencies"),
    path('legal_forms/', LegalFormsList.as_view(), name='legal_forms_list_url'),
    path('legal_form/create/', LegalFormCreate.as_view(), name='legal_form_create_url'),
    path('legal_form/<int:pk>/', LegalFormDetails.as_view(), name='legal_form_details_url'),
    path('legal_form/<int:pk>/update/', LegalFormUpdate.as_view(), name='legal_form_update_url'),
    path('legal_form/<int:pk>/delete/', LegalFormDelete.as_view(), name='legal_form_delete_url'),

]
