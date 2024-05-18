from django.urls import path
import orgsandpeople.views as oview


app_name = "orgsandpeople"

urlpatterns = [
    path('emails/', oview.EmailsList.as_view(), name='emails_list_url'),
    path('email/create/', oview.EmailCreate.as_view(), name='email_create_url'),
    path('email/<int:pk>/update/', oview.EmailUpdate.as_view(), name='email_update_url'),
    path('email/<int:pk>/delete/', oview.EmailDelete.as_view(), name='email_delete_url'),

]
