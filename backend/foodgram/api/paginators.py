from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):

    def paginate_queryset(self, queryset, request, view=None):
        if request.query_params.get('is_in_shopping_cart') == 1:
            page_size = 999
        else:
            page_size = self.get_page_size(request)
        if not page_size:
            return None
        return super().paginate_queryset(queryset, request)
