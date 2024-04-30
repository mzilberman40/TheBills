from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.core.paginator import Paginator
from django.utils.text import slugify
import functools


def inject_values(obj: object, fields: list[str]):
    # добавляет в объект перед передачей в шаблон свойство addons,
    # содержащее список значений свойств объекта из листа fields
    values = list()
    for field in fields:
        v = getattr(obj, field)
        if hasattr(v, 'all'):
            v = [x.__str__() for x in v.all()]
        values.append(v)
    obj.addons = values
    return obj


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
    nav_custom_button = {'name': None, 'show': False}


class ObjectsListMixin(Objects):
    objects_per_page = 1
    query_fields = []
    fields_toshow = []     # fields to show in list
    template_name = 'obj_list.html'
    order_by = None     # List of fields for ordering

    def get(self, request):
        show_query = len(self.query_fields)
        search_query = slugify(request.GET.get('query', ''), allow_unicode=True)
        print(request.GET.get('query', ''), show_query, search_query, self.redirect_to)
        if search_query and self.redirect_to:
            z = [Q((f'{qq}__icontains', search_query)) for qq in self.query_fields]
            print(z)
            q = functools.reduce(lambda a, b: a | b, z)
            print(q)
            objects = self.model.objects.filter(q)
            print(objects)
        else:
            objects = self.model.objects.all()

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
            'nav_custom_button': self.nav_custom_button
        }
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)


class ObjectDetailsMixin(Objects):
    template_name = 'obj_details.html'
    fields_to_header = []
    card_title = None
    fields_to_main = []
    fields_to_footer = []

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        # print(content.get(self.field_to_top_main))
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
            # 'delete_function': self.delete_function_name,
            # 'update_function': self.update_function_name,
            'delete_button': self.delete_button,
            'edit_button': self.edit_button,
            'nav_custom_button': self.nav_custom_button
            # 'base_app_template': self.base_app_template,
        }
        # print(context)
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)


class ObjectCreateMixin(Objects):
    template_name = 'obj_create.html'
    fields_to_fill = []

    def get(self, request):
        form = self.form_model()
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

    def post(self, request):
        bound_form = self.form_model(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            return redirect(self.redirect_to)

        context = {
            'title': self.title,
            'form': bound_form,
            'base_app_template': self.base_app_template,
            'object_create_url': self.create_function_name
        }
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)


class ObjectUpdateMixin(Objects):
    template_name = 'obj_update.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        form = self.form_model(instance=obj)
        context = {
            'title': self.title + f" with pk {obj.pk}.....",
            'form': form,
            # self.model.__name__.lower(): obj,
            'base_app_template': self.base_app_template,
            'object': obj
        }
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        new_dict = request.POST
        bound_form = self.form_model(new_dict, instance=obj)
        if bound_form.is_valid():
            upd_obj = bound_form.save()
            return redirect(self.redirect_to)
        context = {
            'form': bound_form,
            'base_app_template': self.base_app_template,
        }
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)


class ObjectDeleteMixin(Objects):
    template_name = 'obj_delete.html'

    def get(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        context = {
            'object': obj,
            'class_name': self.model.__name__.lower(),
            'object_name': obj.__str__,
            'base_app_template': self.base_app_template,
            'object_redirect_url': self.redirect_to

        }
        context.update(self.additional_context)

        return render(request, self.template_name, context=context)

    def post(self, request, pk):
        obj = get_object_or_404(self.model, pk=pk)
        obj.delete()
        return redirect(reverse(self.redirect_to))
