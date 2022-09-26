from django.http import Http404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from django.utils.text import slugify 

import random
import string


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
    
def get_object_or_none(query, **kwargs):
    try:
        return get_object_or_404(query, **kwargs)
    except:
        return None
    
def random_string_generator(size = 10, chars = string.ascii_lowercase + string.digits): 
    return ''.join(random.choice(chars) for _ in range(size))

def unique_slug_generator(instance,slugField, new_slug = None, size=4): 
    if new_slug is not None: 
        slug = new_slug 
    else: 
        slug = slugify(slugField) 
    Klass = instance.__class__ 
    qs_exists = Klass.objects.filter(slug = slug).exists() 
      
    if qs_exists: 
        new_slug = "{slug}-{randstr}".format( 
            slug = slug, randstr = random_string_generator(size = size)) 
              
        return unique_slug_generator(instance,slugField, new_slug = new_slug) 
    return slug 

def upload_to_uuid(path):
    path_url = '%s/{uuid:base32}{ext}' % path
    return FilePattern(
        filename_pattern=path_url
    )
