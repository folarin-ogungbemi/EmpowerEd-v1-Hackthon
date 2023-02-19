from rest_framework.pagination import PageNumberPagination


class MessagePagination(PageNumberPagination):
    """
    Paginates Message queryset with a page size
    of 50, and a maximum page size of 100.
    """
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100
