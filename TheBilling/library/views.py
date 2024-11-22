import functools
from abc import ABC, abstractmethod

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.utils.text import slugify
from django.views.generic import ListView

from library.inject_values import inject_values


class SilverView(ABC):
    model = None
    form_class = None
    title = ""
    create_function_name = None
    update_function_name = None
    delete_function_name = None
    list_function_name = None
    redirect_to = None
    nav_custom_button_name = "NewItem"
    nav_custom_button_show = True
    nav_custom_button_func = None
    nav_custom_button_param = None

    # success_url = reverse_lazy(list_function_name)
    @abstractmethod
    def get_objects(self):
        pass

    def get_nav_custom_button(self):
        custom_button =  {
        'name': self.nav_custom_button_name,
        'show': self.nav_custom_button_show,
        'func': self.nav_custom_button_func,
        'param': self.nav_custom_button_param,
    }
        return custom_button

class SilverListView(SilverView, ListView):
    title = "Not set"
    query_fields = []
    fields_to_show = []
    redirect_to = None
    paginate_by = 8  # Number of items per page
    view_button = True
    delete_button = True
    edit_button = True

    def get_queryset(self):
        queryset = super().get_queryset()
        show_query = len(self.query_fields)
        search_query = slugify(self.request.GET.get('query', ''), allow_unicode=True)
        if show_query and search_query and self.redirect_to:
            z = [Q((f'{qq}__icontains', search_query)) for qq in self.query_fields]
            q = functools.reduce(lambda a, b: a | b, z)
            queryset = queryset.filter(q)
        return queryset

    def get_objects(self):
        if not self.fields_to_show:
            self.fields_to_show = [f.name for f in self.model._meta.get_fields()]
        #
        return [inject_values(o, self.fields_to_show) for o in self.get_queryset()]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context["show_query"] = len(self.query_fields)
        objects = self.get_objects()

        # Paginator setup
        paginator = Paginator(objects, self.paginate_by)
        page = self.request.GET.get('page', 1)

        try:
            page_objects = paginator.page(page)
        except PageNotAnInteger:
            page_objects = paginator.page(1)
        except EmptyPage:
            page_objects = paginator.page(paginator.num_pages)

        context["paginator"] = paginator
        context["page_object"] = page_objects
        context["is_paginated"] = paginator.num_pages > 1
        context["title"] = self.title
        context["fields_to_show"] = self.fields_to_show
        context["view_button"] = self.view_button
        context["edit_button"] = self.edit_button
        context["delete_button"] = self.delete_button
        context["counter"] = queryset.count()
        context["list_function_name"] = self.list_function_name
        context["create_function_name"] = self.create_function_name
        context["delete_function_name"] = self.delete_function_name
        context["update_function_name"] = self.update_function_name
        context["redirect_to"] = self.redirect_to
        context["nav_custom_button"] = self.get_nav_custom_button()
        return context


