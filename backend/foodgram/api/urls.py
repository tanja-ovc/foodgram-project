from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, PaginatedUserViewSet, RecipeViewSet,
                    TagViewSet)

router = DefaultRouter()


router.register(r'ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register(r'tags', TagViewSet)
router.register(r'users', PaginatedUserViewSet)


urlpatterns = [
    path('', include(router.urls))
]
