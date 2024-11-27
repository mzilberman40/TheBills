from django.urls import path
import commerce.views as cviews

app_name = "commerce"

urlpatterns = [

    # path('resources/', cviews.ResourceList.as_view(), name='resource_list_url_name'),
    # path('resources/create/', cviews.ResourceCreate.as_view(), name='resource_create_url_name'),
    # path('resources/<int:pk>/update/', cviews.ResourceUpdate.as_view(), name='resource_update_url_name'),
    # path('resources/<int:pk>/delete/', cviews.ResourceDelete.as_view(), name='resource_delete_url_name'),
    # path('resources/<int:pk>/', cviews.ResourceDetails.as_view(), name='resource_details_url_name'),
    #
    # path('projects/', cviews.ProjectList.as_view(), name='project_list_url_name'),
    # path('projects/create/', cviews.ProjectCreate.as_view(), name='project_create_url_name'),
    # path('projects/<int:pk>/update/', cviews.ProjectUpdate.as_view(), name='project_update_url_name'),
    # path('projects/<int:pk>/delete/', cviews.ProjectDelete.as_view(), name='project_delete_url_name'),
    # path('projects/<int:pk>/', cviews.ProjectDetails.as_view(), name='project_details_url_name'),
]