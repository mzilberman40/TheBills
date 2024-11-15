from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from commerce.forms import ResourceForm
from commerce.models import *
from library.inject_values import inject_values
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
    fields_toshow = ['name', 'rtype', 'owner', 'available']
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

    # def get(self, request, *args, **kwargs ):
    #     print(args, kwargs)
    #
    #     bu_pk = kwargs.get('bu_pk')
    #     if bu_pk:
    #         bu = get_object_or_404(BusinessUnit, pk=bu_pk)
    #         resources = bu.resources.all()
    #         self.title = f"{bu}'s {self.title}"
    #     else:
    #         resources = self.model.objects.all()
    #
    #     resources = [inject_values(o, self.fields_toshow) for o in resources]
    #
    #     page_number = request.GET.get('page', 1)
    #     paginator = Paginator(resources, self.objects_per_page)
    #     page_object = paginator.get_page(page_number)
    #     is_paginated = page_object.has_other_pages()
    #
    #     self.nav_custom_button['func'] = self.create_function_name
    #     self.nav_custom_button['params'] = bu_pk
    #
    #     context = {
    #         'title': self.title,
    #         'redirect_to': self.redirect_to,
    #         'page_object': page_object,
    #         'is_paginated': is_paginated,
    #         'counter': len(resources),
    #         'fields': self.fields_toshow,
    #         'delete_function': self.delete_function_name,
    #         'update_function': self.update_function_name,
    #         'delete_button': self.delete_button,
    #         'edit_button': self.edit_button,
    #         'view_button': self.view_button,
    #         'nav_custom_button': self.nav_custom_button,
    #     }
    #
    #     return render(request, self.template_name, context=context)


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

