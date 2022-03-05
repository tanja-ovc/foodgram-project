from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from recipes.models import Ingredient
from ..filters import IngredientFilter
from ..serializers import IngredientsListSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientsListSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('^name',)
    filterset_class = IngredientFilter
    permission_classes = (permissions.AllowAny,)
