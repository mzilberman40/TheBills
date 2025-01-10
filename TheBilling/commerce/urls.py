from django.urls import path
import commerce.views as cviews
import commerce.models as cmodels


app_name = "commerce"

urlpatterns = [
    path('projects/', cviews.ProjectList.as_view(), name=cmodels.Project.LOCAL_LIST_URL_NAME()),
    path('projects/create/', cviews.ProjectCreate.as_view(), name=cmodels.Project.LOCAL_CREATE_URL_NAME()),
    path('projects/<int:pk>/update/', cviews.ProjectUpdate.as_view(), name=cmodels.Project.LOCAL_UPDATE_URL_NAME()),
    path('projects/<int:pk>/delete/', cviews.ProjectDelete.as_view(), name=cmodels.Project.LOCAL_DELETE_URL_NAME()),
    path('projects/<int:pk>/', cviews.ProjectDetails.as_view(), name=cmodels.Project.LOCAL_DETAILS_URL_NAME()),

    path('contracts/', cviews.ContractList.as_view(), name=cmodels.Contract.LOCAL_LIST_URL_NAME()),
    path('contracts/create/', cviews.ContractCreate.as_view(), name=cmodels.Contract.LOCAL_CREATE_URL_NAME()),
    path('contracts/<int:pk>/update/', cviews.ContractUpdate.as_view(), name=cmodels.Contract.LOCAL_UPDATE_URL_NAME()),
    path('contracts/<int:pk>/delete/', cviews.ContractDelete.as_view(), name=cmodels.Contract.LOCAL_DELETE_URL_NAME()),
    path('contracts/<int:pk>/', cviews.ContractDetails.as_view(), name=cmodels.Contract.LOCAL_DETAILS_URL_NAME()),

    path('services/', cviews.ServiceList.as_view(), name=cmodels.Service.LOCAL_LIST_URL_NAME()),
    path('services/create/', cviews.ServiceCreate.as_view(), name=cmodels.Service.LOCAL_CREATE_URL_NAME()),
    path('services/<int:pk>/update/', cviews.ServiceUpdate.as_view(), name=cmodels.Service.LOCAL_UPDATE_URL_NAME()),
    path('services/<int:pk>/delete/', cviews.ServiceDelete.as_view(), name=cmodels.Service.LOCAL_DELETE_URL_NAME()),
    path('services/<int:pk>/', cviews.ServiceDetails.as_view(), name=cmodels.Service.LOCAL_DETAILS_URL_NAME()),

    path('Contract/<int:fkey>/services/', cviews.ContractServiceList.as_view(), name='contract_service_list_url_name'),
    path('Contract/<int:fkey>/service/create/', cviews.ContractServiceCreate.as_view(), name='contract_service_create_url_name'),
    path('Contract/<int:fkey>/service/update/<int:pk>/', cviews.ContractServiceUpdate.as_view(),
         name='contract_service_update_url_name'),
    path('Contract/<int:fkey>/service/delete/<int:pk>/', cviews.ContractServiceDelete.as_view(),
         name='contract_service_delete_url_name'),
    path('Contract/<int:fkey>/service/<int:pk>/', cviews.ContractServiceDetails.as_view(),
         name='contract_service_detail_url_name'),

]