from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    django_paginator_class = Paginator
    
    def get_paginated_response(self, data):
        return Response({
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'current_page': self.page.number,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })