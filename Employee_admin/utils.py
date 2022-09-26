from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class ManageBaseView(object):
    method_name = None
    template_name = None
    items_per_page = 10

    def get_template_name(self):
        return self.template_name

    def get(self, request, *args, **kwargs):

        if self.method_name is not None:
            func = getattr(self, self.method_name, None)
            if func is not None:
                return func(request, *args, **kwargs)
        raise Http404("Method Not Allowed")

    def post(self, request, *args, **kwargs):
        if self.method_name is not None:
            func = getattr(self, self.method_name, None)
            if func is not None:
                return func(request, *args, **kwargs)

        raise Http404("Method Not Allowed")

    def get_paginated_items(self, items):
        paginator = Paginator(items, int(self.request.GET.get('records', str(self.items_per_page))))
        page = self.request.GET.get('page', 1)
        try:
            items = paginator.page(page)
        except PageNotAnInteger:
            items = paginator.page(1)
        except EmptyPage:
            items = paginator.page(paginator.num_pages)
        return items