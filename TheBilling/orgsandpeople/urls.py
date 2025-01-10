from django.urls import path
import orgsandpeople.views as oview
import orgsandpeople.models as omodels


app_name = "orgsandpeople"

urlpatterns = [
    path('banks/', oview.BankList.as_view(), name=omodels.Bank.LOCAL_LIST_URL_NAME()),
    path('banks/create/', oview.BankCreate.as_view(), name=omodels.Bank.LOCAL_CREATE_URL_NAME()),
    path('banks/<int:pk>/', oview.BankDetails.as_view(), name=omodels.Bank.LOCAL_DETAILS_URL_NAME()),
    path('banks/<int:pk>/delete/', oview.BankDelete.as_view(), name=omodels.Bank.LOCAL_DELETE_URL_NAME()),
    path('banks/<int:pk>/update/', oview.BankUpdate.as_view(), name=omodels.Bank.LOCAL_UPDATE_URL_NAME()),

    path('emails/', oview.EmailList.as_view(), name=omodels.Email.LOCAL_LIST_URL_NAME()),
    path('emails/create/', oview.EmailCreate.as_view(), name=omodels.Email.LOCAL_CREATE_URL_NAME()),
    path('emails/<int:pk>/', oview.EmailDetails.as_view(), name=omodels.Email.LOCAL_DETAILS_URL_NAME()),
    path('emails/<int:pk>/delete/', oview.EmailDelete.as_view(), name=omodels.Email.LOCAL_DELETE_URL_NAME()),
    path('emails/<int:pk>/update/', oview.EmailUpdate.as_view(), name=omodels.Email.LOCAL_UPDATE_URL_NAME()),

    path('BU/', oview.BusinessUnitList.as_view(), name=omodels.BusinessUnit.LOCAL_LIST_URL_NAME()),
    path('BU/create/', oview.BusinessUnitCreate.as_view(), name=omodels.BusinessUnit.LOCAL_CREATE_URL_NAME()),
    path('BU/<int:pk>/update/', oview.BusinessUnitUpdate.as_view(), name=omodels.BusinessUnit.LOCAL_UPDATE_URL_NAME()),
    path('BU/<int:pk>/delete/', oview.BusinessUnitDelete.as_view(), name=omodels.BusinessUnit.LOCAL_DELETE_URL_NAME()),
    path('BU/<int:pk>/', oview.BusinessUnitDetails.as_view(), name=omodels.BusinessUnit.LOCAL_DETAILS_URL_NAME()),

    path('BU/<int:fkey>/accounts/', oview.BUAccountList.as_view(), name='bu_accounts_url_name'),
    path('BU/<int:fkey>/accounts/create/', oview.BUAccountCreate.as_view(), name='bu_account_create_url_name'),
    path('BU/<int:fkey>/accounts/update/<int:pk>/', oview.BUAccountUpdate.as_view(), name='bu_account_update_url_name'),
    path('BU/<int:fkey>/accounts/delete/<int:pk>/', oview.BUAccountDelete.as_view(), name='bu_account_delete_url_name'),
    path('BU/<int:fkey>/accounts/<int:pk>/', oview.BUAccountDetail.as_view(), name='bu_account_detail_url_name'),

    path('BU/<int:fkey>/resources/', oview.BUResourceList.as_view(), name='bu_resources_url_name'),
    path('BU/<int:fkey>/resources/create/', oview.BUResourceCreate.as_view(), name='bu_resource_create_url_name'),
    path('BU/<int:fkey>/resources/update/<int:pk>/', oview.BUResourceUpdate.as_view(), name='bu_resource_update_url_name'),
    path('BU/<int:fkey>/resources/delete/<int:pk>/', oview.BUResourceDelete.as_view(), name='bu_resource_delete_url_name'),
    path('BU/<int:fkey>/resources/<int:pk>/', oview.BUResourceDetails.as_view(), name='bu_resource_detail_url_name'),

    path('BU/<int:fkey>/contracts/', oview.BUContractList.as_view(), name='bu_contracts_url_name'),
    path('BU/<int:fkey>/contract/create/', oview.BUContractCreate.as_view(), name='bu_contract_create_url_name'),
    path('BU/<int:fkey>/contract/update/<int:pk>/', oview.BUContractUpdate.as_view(),
         name='bu_contract_update_url_name'),
    path('BU/<int:fkey>/contract/delete/<int:pk>/', oview.BUContractDelete.as_view(),
         name='bu_contract_delete_url_name'),
    path('BU/<int:fkey>/contract/<int:pk>/', oview.BUContractDetails.as_view(), name='bu_contract_detail_url_name'),

    path('BU/<int:fkey>/phones/', oview.BUPhoneList.as_view(), name='bu_phones_url_name'),
    path('BU/<int:fkey>/phone/create/', oview.BUPhoneCreate.as_view(), name='bu_phone_create_url_name'),
    path('BU/<int:fkey>/phone/update/<int:pk>/', oview.BUPhoneUpdate.as_view(),
         name='bu_phone_update_url_name'),
    path('BU/<int:fkey>/phone/delete/<int:pk>/', oview.BUPhoneDelete.as_view(),
         name='bu_phone_delete_url_name'),
    path('BU/<int:fkey>/phone/<int:pk>/', oview.BUPhoneDetails.as_view(), name='bu_phone_detail_url_name'),

    #
    # path('BU/<int:fkey>/tgs/', oview.BUTelegramDataList.as_view(), name='bu_telegrams_url_name'),
    # path('BU/<int:fkey>/tg/create/', oview.BUTelegramDataCreate.as_view(), name='bu_telegram_create_url_name'),
    # path('BU/<int:fkey>/tg/update/<int:pk>/', oview.BUTelegramDataUpdate.as_view(),
    #      name='bu_telegram_update_url_name'),
    # path('BU/<int:fkey>/tg/delete/<int:pk>/', oview.BUTelegramDataDelete.as_view(),
    #      name='bu_telegram_delete_url_name'),
    # path('BU/<int:fkey>/tg/<int:pk>/', oview.BUTelegramDataDetails.as_view(), name='bu_telegram_detail_url_name'),

    path('BU/<int:fkey>/emails/', oview.BUEmailList.as_view(), name='bu_emails_url_name'),
    path('BU/<int:fkey>/email/create/', oview.BUEmailCreate.as_view(), name='bu_email_create_url_name'),
    path('BU/<int:fkey>/email/update/<int:pk>/', oview.BUEmailUpdate.as_view(),
         name='bu_email_update_url_name'),
    path('BU/<int:fkey>/email/delete/<int:pk>/', oview.BUEmailDelete.as_view(),
         name='bu_email_delete_url_name'),
    path('BU/<int:fkey>/email/<int:pk>/', oview.BUEmailDetails.as_view(), name='bu_email_details_url_name'),

]
