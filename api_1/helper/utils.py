import uuid 

from django.core.paginator import Paginator as django_core_paginator


def is_valid_uuid(string):
    try:
        uuid_object = uuid.UUID(string)
        return str(uuid_object) == string
    except ValueError:
        return False

class Paginator:

    @staticmethod
    def paginate(request, queryset):
        request_get_data = request.GET
        paginator = django_core_paginator(queryset.order_by("-id"), int(request_get_data.get('size', 10)))
        requested_page = int(request_get_data.get('page', 1))
        verified_page = requested_page if requested_page < paginator.num_pages else paginator.num_pages
        page = paginator.page(verified_page)
        return page
    