from rest_framework.pagination import PageNumberPagination


class Custom999PageNumberPagination(PageNumberPagination):
    page_size = 999
