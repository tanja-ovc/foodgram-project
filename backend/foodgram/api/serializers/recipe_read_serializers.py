from rest_framework import serializers

from recipes.models import IngredientForRecipe, Recipe
from .tag_serializers import TagSerializer
from .user_serializers import CustomUserSerializer


class IngredientForRecipeSerializerRead(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientForRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializerRead(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    ingredients = IngredientForRecipeSerializerRead(
        source='ingredientforrecipe_set', read_only=True, many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'is_favorited', 'is_in_shopping_cart', 'name',
                  'image', 'text', 'cooking_time',)

    def get_is_favorited(self, obj) -> bool:
        current_user = self.context['request'].user
        return obj.favorited_by.filter(id=current_user.id).exists()

    def get_is_in_shopping_cart(self, obj) -> bool:
        current_user = self.context['request'].user
        return obj.in_shopping_cart_of.filter(id=current_user.id).exists()
