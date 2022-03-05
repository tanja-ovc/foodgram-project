from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from recipes.models import IngredientForRecipe, Recipe
from ..filters import RecipeFilter
from ..permissions import IsAuthorOrAuthenticatedOrReadOnlyPermission
from ..serializers import (RecipeSerializerLite, RecipeSerializerRead,
                           RecipeSerializerWrite)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter,)
    permission_classes = (IsAuthorOrAuthenticatedOrReadOnlyPermission,)
    filterset_class = RecipeFilter
    ordering = ('-id',)

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeSerializerRead
        return RecipeSerializerWrite

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['post', 'delete'],
            queryset=Recipe.objects.all(),
            permission_classes=(permissions.IsAuthenticated,))
    # формируемый url для вызова этой функции: recipes/<id>/favorite/
    def favorite(self, request, *args, **kwargs):
        recipe_id = self.kwargs['pk']
        recipe = get_object_or_404(Recipe, id=recipe_id)

        if request.method == 'POST':
            if recipe.is_favorited is False:
                recipe.is_favorited = True
            else:
                return Response(
                    {'detail': 'Этот рецепт уже есть в вашем избранном.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if request.method == 'DELETE':
            if recipe.is_favorited is True:
                recipe.is_favorited = False
            else:
                return Response(
                    {'detail': 'Этого рецепта нет в вашем избранном.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if request.method not in ['POST', 'DELETE']:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        serializer = RecipeSerializerLite(
            recipe, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if request.method == 'POST':
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED,
                headers=headers
            )
        if request.method == 'DELETE':
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True,
            methods=['post', 'delete'],
            queryset=Recipe.objects.all(),
            permission_classes=(permissions.IsAuthenticated,))
    # формируемый url для вызова этой функции: recipes/<id>/shopping_cart/
    def shopping_cart(self, request, *args, **kwargs):

        recipe_id = self.kwargs['pk']
        recipe = get_object_or_404(Recipe, id=recipe_id)

        if request.method == 'POST':
            if recipe.is_in_shopping_cart is False:
                recipe.is_in_shopping_cart = True
            else:
                return Response(
                    {'detail': 'Этот рецепт уже есть в вашем списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if request.method == 'DELETE':
            if recipe.is_in_shopping_cart is True:
                recipe.is_in_shopping_cart = False
            else:
                return Response(
                    {'detail': 'Этого рецепта нет в вашем списке покупок.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if request.method not in ['POST', 'DELETE']:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        serializer = RecipeSerializerLite(
            recipe, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        if request.method == 'POST':
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED,
                headers=headers
            )
        if request.method == 'DELETE':
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False,
            methods=['get'],
            permission_classes=(permissions.IsAuthenticated,))
    # формируемый url для вызова этой функции: recipes/download_shopping_cart/
    def download_shopping_cart(self, request):
        ingredients_in_my_cart = IngredientForRecipe.objects.filter(
            recipe__is_in_shopping_cart=True).values(
                'ingredient__name', 'ingredient__measurement_unit').annotate(
                    total_amount=Sum('amount'))
        if not ingredients_in_my_cart:
            return Response(
                    {'detail': 'В вашем списке покупок пока нет рецептов.'},
                    status=status.HTTP_400_BAD_REQUEST)
        ingredients_list = []
        for ingredient_obj in ingredients_in_my_cart:
            name = ingredient_obj['ingredient__name']
            total_amount = ingredient_obj['total_amount']
            measurement_unit = ingredient_obj['ingredient__measurement_unit']
            ingredient_list_view = (
                f'{name} - {total_amount} {measurement_unit}'
            )
            ingredients_list.append(ingredient_list_view)
        response = Response(ingredients_list, status=status.HTTP_201_CREATED,
                            content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="list.txt"'
        return response
