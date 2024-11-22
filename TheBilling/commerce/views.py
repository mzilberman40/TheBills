from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from commerce.forms import ResourceForm, ProjectForm
from commerce.models import *
from library.inject_values import inject_values
from utils import ObjectsListMixin, ObjectDetailsMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin


class Commerce(LoginRequiredMixin):
    # base_app_template = 'commerce/base_orgs_and_people.html'
    raise_exception = True
    objects_per_page = 8


class Resources(Commerce):
    model = Resource
    form_model = ResourceForm
    form_class = ResourceForm
    title = "Resources"
    create_function_name = 'commerce:resource_create_url'
    update_function_name = 'commerce:resource_update_url'
    delete_function_name = 'commerce:resource_delete_url'
    list_function_name = 'commerce:resource_list_url'
    redirect_to = list_function_name
    success_url = reverse_lazy(list_function_name)
    params = {'redirect_param': 'bu_pk', 'update_param': 'pk', 'delete_param': 'pk'}


class ResourceList(Resources, ObjectsListMixin):
    fields_to_show = ['name', 'rtype', 'owner', 'available']
    query_fields = ['name', 'rtype', 'owner']
    order_by = 'name'
    template_name = 'obj_list.html'
    edit_button = True
    view_button = True
    delete_button = True
    nav_custom_button = {
        'name': 'NewItem',
        'show': True,
        'func': Resources.create_function_name,
    }

class ResourceDetails(Resources, ObjectDetailsMixin):
    edit_button = True
    title = "Resource Details"
    fields_to_header = ['id', 'rtype', 'name', 'owner']
    fields_to_main = [ 'description', 'available']
    fields_to_footer = ['created', 'modified', 'user']


class ResourceCreate(Resources, ObjectCreateMixin):
    title = "Resource Create"


class ResourceUpdate(Resources, ObjectUpdateMixin):
    title = "Updating email"


class ResourceDelete(Resources, ObjectDeleteMixin):
    pass


class Projects(Commerce):
    model = Project
    form_class = ProjectForm
    title = "Projects"
    create_function_name = 'commerce:project_create_url'
    update_function_name = 'commerce:project_update_url'
    delete_function_name = 'commerce:project_delete_url'
    list_function_name = 'commerce:project_list_url'
    redirect_to = list_function_name
    success_url = reverse_lazy(list_function_name)


class ProjectList(Projects, ObjectsListMixin):
    fields_to_show = ['title', 'beneficiary']
    query_fields = ['title']
    order_by = 'title'
    template_name = 'obj_list.html'
    nav_custom_button = {'name': 'NewItem', 'show': True}
    edit_button = True
    view_button = True
    delete_button = True


class ProjectDetails(Projects, ObjectDetailsMixin):
    title = f"Project Details"
    fields_to_header = ['id', 'title', 'beneficiary']
    fields_to_main = ['description']
    fields_to_footer = []


class ProjectCreate(Projects, ObjectCreateMixin):
    title = "Project Create"


class ProjectUpdate(Projects, ObjectUpdateMixin):
    title = "Updating Project"


class ProjectDelete(Projects, ObjectDeleteMixin):
    template_name = 'obj_delete.html'
    title = "Deleting Project"
