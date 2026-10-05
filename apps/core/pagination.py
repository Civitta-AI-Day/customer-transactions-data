from rest_framework.pagination import PageNumberPagination


class StandardPagination(PageNumberPagination):
    """Default pagination for every list endpoint: ?page=N&page_size=M (max 200)."""

    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 200
