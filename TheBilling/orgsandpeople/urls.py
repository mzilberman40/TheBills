from django.urls import path
import orgsandpeople.views as oview
import commerce.views as comview


app_name = "orgsandpeople"

urlpatterns = [
    path('banks/', oview.BankList.as_view(), name='bank_list_url'),
    path('banks/create/', oview.BankCreate.as_view(), name='bank_create_url'),
    path('banks/<int:pk>/', oview.BankDetails.as_view(), name='bank_details_url'),
    path('banks/<int:pk>/delete/', oview.BankDelete.as_view(), name='bank_delete_url'),
    path('banks/<int:pk>/update/', oview.BankUpdate.as_view(), name='bank_update_url'),

    path('BU/', oview.BusinessUnitList.as_view(), name='bu_list_url'),
    path('BU/create/', oview.BusinessUnitCreate.as_view(), name='bu_create_url'),
    path('BU/<int:pk>/update/', oview.BusinessUnitUpdate.as_view(), name='bu_update_url'),
    path('BU/<int:pk>/delete/', oview.BusinessUnitDelete.as_view(), name='bu_delete_url'),
    path('BU/<int:pk>/', oview.BusinessUnitDetails.as_view(), name='bu_details_url'),

    path('BU/<int:bu_pk>/accounts/', oview.BUAccountList.as_view(), name='bu_accounts_url'),
    path('BU/<int:bu_pk>/accounts/create/', oview.BUAccountCreate.as_view(), name='bu_account_create_url'),
    path('BU/<int:bu_pk>/accounts/update/<int:pk>/', oview.BUAccountUpdate.as_view(), name='bu_account_update_url'),
    path('BU/<int:bu_pk>/accounts/delete/<int:pk>/', oview.BUAccountDelete.as_view(), name='bu_account_delete_url'),
    path('BU/<int:bu_pk>/accounts/<int:pk>/', oview.BUAccountDetail.as_view(), name='bu_account_detail_url'),

    path('BU/<int:bu_pk>/resources/', comview.ResourceList.as_view(), name='bu_resources_url'),
    path('BU/<int:bu_pk>/resources/create/', comview.ResourceCreate.as_view(), name='bu_resource_create_url'),
    path('BU/<int:bu_pk>/resources/update/<int:pk>/', comview.ResourceUpdate.as_view(), name='bu_resource_update_url'),
    path('BU/<int:bu_pk>/resources/delete/<int:pk>/', comview.ResourceDelete.as_view(), name='bu_resource_delete_url'),
    path('BU/<int:bu_pk>/resources/<int:pk>/', comview.ResourceDetails.as_view(), name='bu_resource_detail_url'),
]