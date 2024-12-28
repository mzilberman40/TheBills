
from django.db.models import Q, ProtectedError
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.utils.text import slugify
import functools
from django.views.generic import View
from django.contrib import messages

from library.Param import Param
from library.field_name2model import field_name2model
from library.inject_values import inject_values


def filter_fields(form, fields_to_show=None, fields_to_exclude=None):
    """
    Filters the form's fields to only include those specified in `fields_to_fill`.
    """
    form.fields = {key: value for key, value in form.fields.items()
                   if key in fields_to_show and key not in fields_to_exclude}


class Objects:
    template_name = None
    model = None
    base_app_template = None
    form_class = None
    create_url_name = None
    delete_url_name = None
    details_url_name = None
    update_url_name = None
    list_url_name = None
    redirect_url_name = None
    success_url_name = None
    fail_url_name = None
    fk_param = Param(field_name=None, key=None)
    redirect_param = Param(field_name=None, key=None)
    filter_param = Param(field_name=None, key=None)
    create_param = Param(field_name=None, key=None)
    update_param = Param(field_name=None, key=None)
    title = 'No title'
    comments = ''
    additional_context = {}
    edit_button = True
    delete_button = True
    view_button = True
    nav_custom_button = {
        'name': None,
        'show': False,
        'func': None,
    }
    # params = {}

    @staticmethod
    def get_kwargs(param: Param, obj, **kwargs) -> dict:
        if param.key:
            value = kwargs.get(param.key)
            if value:
                return {param.key: value}

            if param.field_name:
                value = getattr(obj, param.field_name, None)
                if value:
                    return {param.key: value}

        return {}


class ObjectsListMixin(Objects, View):
    objects_per_page = 1
    query_fields = []
    fields_to_show = []     # fields to show in list
    template_name = 'obj_list.html'
    order_by = None     # List of fields for ordering
    nav_custom_button_func = None

    def get(self, request, **kwargs):
        # print(kwargs)
        queryset = self.model.objects.all()
        title = self.title
        self.nav_custom_button['func'] = reverse_lazy(self.nav_custom_button_func)
        # print(self.filter_param)
        fk_value = None
        if self.filter_param:
            fk_value = kwargs.get(self.filter_param.key, None)
            if fk_value:
                queryset = queryset.filter(**{self.filter_param.field_name: fk_value})
                related_model = field_name2model(self.model, self.filter_param.field_name)
                related_object = related_model.objects.get(pk=fk_value)
                title = f"{title} of {related_object}"
                # print("Create_params: ", {self.filter_param.key: fk_value})
                self.nav_custom_button['func'] = (
                    reverse_lazy(self.nav_custom_button_func, kwargs={self.filter_param.key: fk_value}))

        show_query = len(self.query_fields)
        search_query = slugify(request.GET.get('query', ''), allow_unicode=True)
        if search_query and self.redirect_url_name:
            z = [Q((f'{qq}__icontains', search_query)) for qq in self.query_fields]
            q = functools.reduce(lambda a, b: a | b, z)
            queryset = queryset.filter(q)

        if self.order_by:
            queryset = queryset.order_by(self.order_by)

        if not self.fields_to_show:
            self.fields_to_show = [f.name for f in self.model._meta.get_fields()]
        #
        objects = [inject_values(o, self.fields_to_show) for o in queryset]
        page_number = request.GET.get('page', 1)
        paginator = Paginator(objects, self.objects_per_page)
        page_object = paginator.get_page(page_number)
        is_paginated = page_object.has_other_pages()

        context = {
            'title': title,
            'comments': self.comments,
            'base_app_template': self.base_app_template,
            'show_query': show_query,
            'redirect_url': reverse_lazy(self.redirect_url_name, kwargs=kwargs),
            # 'delete_url': reverse_lazy(self.delete_url_name, kwargs=kwargs),
            # 'update_url': reverse_lazy(self.update_url_name, kwargs=kwargs),
            # 'details_url': reverse_lazy(self.details_url_name, kwargs=kwargs),
            'details_url_name': self.details_url_name,
            'delete_url_name': self.delete_url_name,
            'update_url_name': self.update_url_name,
            'fkey': self.filter_param.key if self.filter_param else None,
            'fvalue': fk_value if fk_value else None,

            # For search
            'search_query': search_query,
            'page_object': page_object,
            'is_paginated': is_paginated,
            'counter': len(objects),
            'fields': self.fields_to_show,
            'delete_button': self.delete_button,
            'edit_button': self.edit_button,
            'view_button': self.view_button,
            'nav_custom_button': self.nav_custom_button,
        }
        context.update(self.additional_context)
        print("Context for list:", context)

        return render(request, self.template_name, context=context)


class ObjectDetailsMixin(Objects, View):
    template_name = 'obj_details.html'
    fields_to_header = []
    card_title = None
    fields_to_main = []
    fields_to_footer = []
    fk_value = None

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        obj = get_object_or_404(self.model, pk=pk)
        if self.filter_param:
            self.fk_value = kwargs.get(self.filter_param.key, None)

        redirect_kwargs = self.get_kwargs(self.redirect_param, obj, **kwargs)
        # print(redirect_kwargs)

        header_dict = {k: getattr(obj, k, None) for k in self.fields_to_header}
        main_dict = {k: getattr(obj, k, None) for k in self.fields_to_main}
        footer_dict = {k: getattr(obj, k, None) for k in self.fields_to_footer}

        context = {
            'title': f'{self.title}: {obj} ',
            f'{self.model.__name__.lower()}': obj,
            'model_name': f'{self.model.__name__.lower()}',
            'object': obj,
            'admin_object': obj,
            'header_dict': header_dict,
            'card_title': self.card_title,
            'main_dict': main_dict,
            'footer_dict': footer_dict,
            'details': True,
            'details_url_name': self.details_url_name,
            'delete_url_name': self.delete_url_name,
            'update_url_name': self.update_url_name,
            'redirect_url': reverse_lazy(self.redirect_url_name, kwargs=redirect_kwargs),  # For button "Cancel"
            'delete_button': self.delete_button,
            'edit_button': self.edit_button,
            'fvalue': self.fk_value
        }
        context.update(kwargs)
        context.update(self.additional_context)
        print("Context for details:", context)

        return render(request, self.template_name, context=context)


class ObjectCreateMixin(Objects, View):

    template_name = 'obj_create.html'
    fields_to_fill = []
    fields_to_exclude = []
    create_param = None

    def get(self, request, **kwargs):
        print(f"Create method kwargs: {kwargs}")
        form = self.form_class()
        if self.create_param:
            field_name = self.create_param.field_name
            field_value = kwargs.get(self.filter_param.key, None)
            if field_value:
                self.fields_to_exclude.append(field_name)

        fields_to_fill = self.fields_to_fill or form.fields.keys()
        print(fields_to_fill)
        filter_fields(form, fields_to_fill, self.fields_to_exclude)

        context = {
            'title': self.title,
            'form': form,
            'base_app_template': self.base_app_template,
            # 'class_name': self.model.__name__.lower(),
            'redirect_url': reverse_lazy(self.redirect_url_name, kwargs=kwargs)
        }

        context.update(self.additional_context)
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        data = request.POST.copy()  # Make a mutable copy of POST data

        if self.filter_param:
            field_name = self.filter_param.field_name
            field_value = kwargs.get(self.filter_param.key, None)
            print(f"POST method kwargs: {field_name}, {field_value}")
            data[field_name] = field_value

        self.success_url = reverse_lazy(self.success_url_name, kwargs=kwargs)
        form = self.form_class(data)
        if form.is_valid():
            form.instance.user = self.request.user
            form.save()
            return redirect(self.success_url)

        # If the form is invalid, re-render it with the same context
        context = {
            'title': self.title,
            'form': form,  # Bound form with validation errors
        }
        context.update(self.additional_context)
        return render(request, self.template_name, context)


class ObjectUpdateMixin(Objects, View):
    template_name = 'obj_update.html'

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_class(instance=obj)
        redirect_kwargs = self.get_kwargs(self.redirect_param, obj, **kwargs)
        # print(redirect_kwargs)

        context = {
            'title': self.title + f" with pk {obj.pk}.....",
            'form': form,
            'object': obj,
            'redirect_url': reverse_lazy(self.redirect_url_name, kwargs=redirect_kwargs), # For Cancel button
        }
        context.update(self.additional_context)
        # print(context)
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        obj = get_object_or_404(self.model, pk=pk)
        redirect_kwargs = self.get_kwargs(self.redirect_param, obj, **kwargs)

        self.success_url = reverse_lazy(self.success_url_name, kwargs=redirect_kwargs)
        bound_form = self.form_class(request.POST.copy(), instance=obj)

        if bound_form.is_valid():
            bound_form.save()
            return redirect(self.success_url)

        context = {
            'form': bound_form,
        }
        context.update(self.additional_context)
        return render(request, self.template_name, context=context)

class ObjectDeleteMixin(Objects, View):
    template_name = 'obj_delete.html'

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        obj = get_object_or_404(self.model, pk=pk)
        if not self.redirect_url_name:
            self.redirect_url_name = self.list_url_name

        redirect_kwargs = self.get_kwargs(self.redirect_param, obj, **kwargs)

        context = {
            'obj': obj,
            'class_name': self.model.__name__.lower(),
            'object_name': str(obj),
            'base_app_template': self.base_app_template,
            'redirect_url': reverse_lazy(self.redirect_url_name, kwargs=redirect_kwargs),
        }
        # print(redirect_kwargs)
        context.update(self.additional_context)
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        pk = kwargs.get('pk')
        obj = get_object_or_404(self.model, pk=pk)
        redirect_kwargs = self.get_kwargs(self.redirect_param, obj, **kwargs)

        try:
            obj.delete()
            messages.success(request, f"{str(obj)} deleted successfully.")
        except ProtectedError:
            # Handling the case where deletion is not possible due to protected references
            messages.error(request, f"Cannot delete {obj}  because it is being referenced by other business units.")
            return redirect(self.redirect_url_name)

        redirect_url = reverse_lazy(self.redirect_url_name, kwargs=redirect_kwargs)
        return redirect(redirect_url)
