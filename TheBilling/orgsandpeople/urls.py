from django.urls import path
import orgsandpeople.views as oview
import commerce.views as comview


app_name = "orgsandpeople"

urlpatterns = [
    path('banks/', oview.BankList.as_view(), name='bank_list_url_name'),
    path('banks/create/', oview.BankCreate.as_view(), name='bank_create_url_name'),
    path('banks/<int:pk>/', oview.BankDetails.as_view(), name='bank_details_url_name'),
    path('banks/<int:pk>/delete/', oview.BankDelete.as_view(), name='bank_delete_url_name'),
    path('banks/<int:pk>/update/', oview.BankUpdate.as_view(), name='bank_update_url_name'),

    path('BU/', oview.BusinessUnitList.as_view(), name='bu_list_url_name'),
    path('BU/create/', oview.BusinessUnitCreate.as_view(), name='bu_create_url_name'),
    path('BU/<int:pk>/update/', oview.BusinessUnitUpdate.as_view(), name='bu_update_url_name'),
    path('BU/<int:pk>/delete/', oview.BusinessUnitDelete.as_view(), name='bu_delete_url_name'),
    path('BU/<int:pk>/', oview.BusinessUnitDetails.as_view(), name='bu_details_url_name'),

    path('BU/<int:bu_pk>/accounts/', oview.BUAccountList.as_view(), name='bu_accounts_url_name'),
    path('BU/<int:bu_pk>/accounts/create/', oview.BUAccountCreate.as_view(), name='bu_account_create_url_name'),
    path('BU/<int:bu_pk>/accounts/update/<int:pk>/', oview.BUAccountUpdate.as_view(), name='bu_account_update_url_name'),
    path('BU/<int:bu_pk>/accounts/delete/<int:pk>/', oview.BUAccountDelete.as_view(), name='bu_account_delete_url_name'),
    path('BU/<int:bu_pk>/accounts/<int:pk>/', oview.BUAccountDetail.as_view(), name='bu_account_detail_url_name'),

    path('BU/<int:bu_pk>/resources/', oview.BUResourceList.as_view(), name='bu_resources_url_name'),
    path('BU/<int:bu_pk>/resources/create/', oview.BUResourceCreate.as_view(), name='bu_resource_create_url_name'),
    path('BU/<int:bu_pk>/resources/update/<int:pk>/', oview.BUResourceUpdate.as_view(), name='bu_resource_update_url_name'),
    path('BU//<int:bu_pk>/resources/delete/<int:pk>/', oview.BUResourceDelete.as_view(), name='bu_resource_delete_url_name'),
    path('BU//<int:bu_pk>/resources/<int:pk>/', oview.BUResourceDetails.as_view(), name='bu_resource_detail_url_name'),
]