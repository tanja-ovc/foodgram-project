from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe

TAGS_CHOICES = (
    ('breakfast', 'завтрак'),
    ('lunch', 'обед'),
    ('dinner', 'ужин'),
)


class RecipeFilter(filters.FilterSet):
    tags = filters.MultipleChoiceFilter(
        lookup_expr='slug__iexact', choices=TAGS_CHOICES
    )
    author = filters.CharFilter(lookup_expr='id__iexact')

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'tags', 'author',)


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
