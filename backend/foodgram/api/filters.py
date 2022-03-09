from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe
from tags.models import Tag


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(filters.FilterSet):
    tags = filters.MultipleChoiceFilter(
        lookup_expr='slug__iexact', choices=Tag.TAGS_CHOICES
    )
    author = filters.CharFilter(lookup_expr='id__iexact')
    is_favorited = filters.NumberFilter(
        field_name='favorited_by', method='filter_is_favorited'
    )
    is_in_shopping_cart = filters.NumberFilter(
        field_name='in_shopping_cart_of', method='filter_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('is_favorited', 'is_in_shopping_cart', 'tags', 'author',)

    def filter_added_objects(self, queryset, name, value,
                             added_recipes, not_added_recipes):
        if not self.request.user.is_authenticated:
            return queryset.none()
        if value == 1:
            return added_recipes
        if value == 0:
            return not_added_recipes
        else:
            return queryset.none()

    def filter_is_favorited(self, queryset, name, value):
        added_recipes = queryset.filter(
            favorited_by__id=self.request.user.id)
        not_added_recipes = queryset.exclude(
            favorited_by__id=self.request.user.id)
        return self.filter_added_objects(
            queryset, name, value, added_recipes, not_added_recipes)

    def filter_is_in_shopping_cart(self, queryset, name, value):
        added_recipes = queryset.filter(
            in_shopping_cart_of__id=self.request.user.id)
        not_added_recipes = queryset.exclude(
            in_shopping_cart_of__id=self.request.user.id)
        return self.filter_added_objects(
            queryset, name, value, added_recipes, not_added_recipes)
