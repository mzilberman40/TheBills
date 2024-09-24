from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from commerce.forms import ResourceForm
from commerce.models import *
from utils import ObjectsListMixin, ObjectDetailsMixin, ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin


class Commerce(LoginRequiredMixin):
    # base_app_template = 'commerce/base_orgs_and_people.html'
    raise_exception = True
    objects_per_page = 8
    edit_button = False
    delete_button = False
    view_button = False


class Resources(Commerce):
    model = Resource
    form_model = ResourceForm
    title = "Resources"
    create_function_name = 'commerce:resource_create_url'
    update_function_name = 'commerce:resource_update_url'
    delete_function_name = 'commerce:resource_delete_url'
    list_function_name = 'commerce:resource_list_url'
    redirect_to = list_function_name


class ResourceList(Resources, ObjectsListMixin, View):
    fields_toshow = ['name', 'group', 'available']
    query_fields = ['name', 'group']
    order_by = 'name'
    template_name = 'obj_list.html'
    edit_button = True
    delete_button = True
    nav_custom_button = {
        'name': 'NewItem',
        'show': True,
        'func': Resources.create_function_name,
    }


class ResourceDetails(Resources, ObjectDetailsMixin, View):
    title = "Resource Details"
    template_name = 'obj_list.html'


class ResourceCreate(Resources, ObjectCreateMixin, View):
    title = "Resource Create"


class ResourceUpdate(Resources, ObjectUpdateMixin, View):
    title = "Updating email"


class ResourceDelete(Resources, ObjectDeleteMixin, View):
    pass

