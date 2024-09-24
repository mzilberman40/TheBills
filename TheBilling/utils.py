from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, reverse
# from django.http.request import QueryDict, MultiValueDict
from django.core.paginator import Paginator
from django.utils.text import slugify
import functools

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, TemplateView, View

from library.inject_values import inject_values


class Objects:
    template_name = None
    model = None
    base_app_template = None
    form_model = None
    # object_redirect_url = None  # deprecated
    # request_proc = do_nothing
    create_function_name = None
    delete_function_name = None
    update_function_name = None
    list_function_name = None
    redirect_to = None
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
        'params': None,
    }
    params = {}


class ObjectsListMixin(Objects, ListView):
    objects_per_page = 1
    query_fields = []
    fields_toshow = []     # fields to show in list
    template_name = 'obj_list.html'
    order_by = None     # List of fields for ordering
    # filter_key = ()

    def get(self, request, **kwargs):
        show_query = len(self.query_fields)
        search_query = slugify(request.GET.get('query', ''), allow_unicode=True)
        queryset = self.model.objects.all()
        if search_query and self.redirect_to:
            z = [Q((f'{qq}__icontains', search_query)) for qq in self.query_fields]
            q = functools.reduce(lambda a, b: a | b, z)
            objects = queryset.filter(q)
        else:
            objects = queryset

        if self.order_by:
            objects = objects.order_by(self.order_by)

        if not self.fields_toshow:
            self.fields_toshow = [f.name for f in self.model._meta.get_fields()]
        #
        objects = [inject_values(o, self.fields_toshow) for o in objects]
        page_number = request.GET.get('page', 1)
        paginator = Paginator(objects, self.objects_per_page)
        page_object = paginator.get_page(page_number)
        is_paginated = page_object.has_other_pages()
        self.nav_custom_button['func'] = self.create_function_name

        context = {
            'title': self.title,
            'comments': self.comments,
            'base_app_template': self.base_app_template,
            'show_query': show_query,
            'redirect_to': self.redirect_to,
            'search_query': search_query,
            'page_object': page_object,
            'is_paginated': is_paginated,
            'counter': len(objects),
            'fields': self.fields_toshow,
            'create_function': self.create_function_name,
            'delete_function': self.delete_function_name,
            'update_function': self.update_function_name,
            'delete_button': self.delete_button,
            'edit_button': self.edit_button,
            'view_button': self.view_button,
            'nav_custom_button': self.nav_custom_button,

        }
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)


class ObjectDetailsMixin(Objects, View):
    template_name = 'obj_details.html'
    fields_to_header = []
    card_title = None
    fields_to_main = []
    fields_to_footer = []

    def get(self, request, pk, **kwargs):
        redirect_param = self.params.get('redirect_param')

        obj = get_object_or_404(self.model, pk=pk)
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
            'list_function': self.list_function_name,
            'delete_function': self.delete_function_name,
            'update_function': self.update_function_name,
            'object_update_url': self.update_function_name,
            'delete_button': self.delete_button,
            'edit_button': self.edit_button,
            'redirect_param': kwargs.get(redirect_param)
        }
        context.update(kwargs)
        # print(context)
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)


class ObjectCreateMixin(Objects, CreateView):
    template_name = 'obj_create.html'
    fields_to_fill = []

    def get(self, request, **kwargs):
        form = self.form_class()
        if self.fields_to_fill:
            form.fields = {key: value for key, value in form.fields.items() if key in self.fields_to_fill}
        context = {
            'title': self.title,
            'form': form,
            'base_app_template': self.base_app_template,
            'class_name': self.model.__name__.lower(),
            'object_create_url': self.create_function_name
        }
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)

        # If the form is invalid, re-render it with the same context
        context = {
            'title': self.title,
            'form': form,  # Bound form with validation errors
            'base_app_template': self.base_app_template,
            'object_create_url': self.create_function_name
        }
        context.update(self.additional_context)
        return render(request, self.template_name, context)

    def form_valid(self, form):
        # Assign the user to the form instance
        form.instance.user = self.request.user
        return super().form_valid(form)


class ObjectUpdateMixin(Objects, UpdateView):
    template_name = 'obj_update.html'

    def get(self, request, pk, **kwargs):
        obj = get_object_or_404(self.model, pk=pk)
        redirect_param = self.params.get('redirect_param')
        # print(kwargs)

        form = self.form_model(instance=obj)
        context = {
            'title': self.title + f" with pk {obj.pk}.....",
            'form': form,
            # self.model.__name__.lower(): obj,
            # 'base_app_template': self.base_app_template,
            'object': obj,
            'update_function': self.update_function_name,
            'redirect_param': kwargs.get(redirect_param)
        }
        context.update(self.additional_context)
        # print(context)

        return render(request, self.template_name, context=context)

    def post(self, request, pk, **kwargs):
        args = []
        obj = get_object_or_404(self.model, pk=pk)
        new_data = request.POST.copy()  # Make a mutable copy of POST data
        new_data['user'] = request.user  # Probably user is necessary for model
        bound_form = self.form_model(new_data, instance=obj)
        redirect_param = self.params.get('redirect_param')
        if redirect_param:
            args.append(kwargs.get(redirect_param))
        if bound_form.is_valid():
            bound_form.save()
            return redirect(self.redirect_to, *args)
        context = {
            'form': bound_form,
            'base_app_template': self.base_app_template,
            'redirect_param': kwargs.get(redirect_param)

        }
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)


class ObjectDeleteMixin(Objects, DeleteView):
    template_name = 'obj_delete.html'

    def get(self, request, pk, **kwargs):
        # print('GET', kwargs)
        obj = get_object_or_404(self.model, pk=pk)
        redirect_param = self.params.get('redirect_param')

        context = {
            'object': obj,
            'class_name': self.model.__name__.lower(),
            'object_name': obj.__str__,
            'base_app_template': self.base_app_template,
            'object_redirect_url': self.redirect_to,
            'redirect_param': kwargs.get(redirect_param),
        }
        context.update(self.additional_context)
        return render(request, self.template_name, context=context)

    def post(self, request, pk, **kwargs):
        # print('POST', kwargs)
        redirect_param = kwargs.get(self.params.get('redirect_param'))

        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        # print('POST', kwargs, redirect_param)

        return redirect(reverse(self.redirect_to, kwargs=kwargs))
