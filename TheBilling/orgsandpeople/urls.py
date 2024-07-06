from django.urls import path
import orgsandpeople.views as oview


app_name = "orgsandpeople"

urlpatterns = [
    # path('emails/', oview.EmailsList.as_view(), name='emails_list_url'),
    # path('email/create/', oview.EmailCreate.as_view(), name='email_create_url'),
    # path('email/<int:pk>/update/', oview.EmailUpdate.as_view(), name='email_update_url'),
    # path('email/<int:pk>/delete/', oview.EmailDelete.as_view(), name='email_delete_url'),

    path('BU/', oview.BusinessUnitList.as_view(), name='bu_list_url'),
    path('BU/create/', oview.BusinessUnitCreate.as_view(), name='bu_create_url'),
    path('BU/<int:pk>/update/', oview.BusinessUnitUpdate.as_view(), name='bu_update_url'),
    path('BU/<int:pk>/delete/', oview.BusinessUnitDelete.as_view(), name='bu_delete_url'),

]
