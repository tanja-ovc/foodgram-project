from rest_framework import serializers

from recipes.models import Recipe


class RecipeSerializerLite(serializers.ModelSerializer):
    """
    A "lite" version of RecipeSerializer: serializes only 4 fields.
    Read only.
    """

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
