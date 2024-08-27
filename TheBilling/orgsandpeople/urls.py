from django.urls import path
import orgsandpeople.views as oview


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

    # path('Accounts/', oview.AccountList.as_view(), name='account_list_url'),
    # path('Account/create/', oview.AccountCreate.as_view(), name='account_create_url'),
    # path('Account/<int:pk>/update/', oview.AccountUpdate.as_view(), name='account_update_url'),
    # path('Account/<int:pk>/delete/', oview.AccountDelete.as_view(), name='account_delete_url'),
    # path('Account/<int:pk>/', oview.AccountDetails.as_view(), name='account_details_url'),
]
