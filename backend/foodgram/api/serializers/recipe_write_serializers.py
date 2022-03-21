from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from recipes.models import Ingredient, IngredientForRecipe, Recipe
from tags.models import Tag
from .user_serializers import CustomUserSerializer


class IngredientForRecipeSerializerWrite(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientForRecipe
        fields = ('id', 'amount')

    def to_representation(self, value):
        return {
            "id": value.ingredient.id,
            "ingredient": value.ingredient.name,
            "measurement_unit": value.ingredient.measurement_unit,
            "amount": value.amount
        }


class TagsRepresentationField(serializers.PrimaryKeyRelatedField):

    def to_representation(self, value):
        return {
            "id": value.id,
            "name": value.name,
            "color": value.color,
            "slug": value.slug
        }


class RecipeSerializerWrite(serializers.ModelSerializer):
    tags = TagsRepresentationField(
        queryset=Tag.objects.all(), many=True
    )
    ingredients = IngredientForRecipeSerializerWrite(
        source='ingredientforrecipe_set', many=True
    )
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients',
                  'name', 'image', 'text', 'cooking_time')

    def create(self, validated_data):
        ingredients_for_recipe = validated_data.pop('ingredientforrecipe_set')
        tags_for_recipe = validated_data.pop('tags')

        recipe = Recipe.objects.create(**validated_data)

        for tag in tags_for_recipe:
            checked_tag = get_object_or_404(Tag, id=tag.id)
            recipe.tags.add(checked_tag)

        for ingredient in ingredients_for_recipe:
            checked_ingredient = get_object_or_404(
                Ingredient, id=ingredient['id']
            )
            ingredient_exists = IngredientForRecipe.objects.filter(
                recipe=recipe, ingredient=checked_ingredient
            ).exists()
            if ingredient_exists:
                raise serializers.ValidationError(
                    'Вы добавили один ингредиент несколько раз.'
                )
            IngredientForRecipe.objects.create(
                recipe=recipe, ingredient=checked_ingredient,
                amount=ingredient['amount']
            )
        return recipe

    def update(self, instance, validated_data):

        if validated_data.get('ingredientforrecipe_set'):
            ingredients_for_recipe = validated_data.pop(
                'ingredientforrecipe_set'
            )
            new_ingredients = []

            for ingredient in ingredients_for_recipe:
                checked_ingredient = get_object_or_404(
                    Ingredient, id=ingredient['id']
                )
                new_ingredient_exists = IngredientForRecipe.objects.filter(
                    recipe=instance, ingredient=checked_ingredient
                ).exists()

                if new_ingredient_exists:
                    raise serializers.ValidationError(
                        'Вы добавили один ингредиент несколько раз.'
                    )
                IngredientForRecipe.objects.create(
                    recipe=instance, ingredient=checked_ingredient,
                    amount=ingredient['amount']
                )
                new_ingredients.append(checked_ingredient)

            instance.ingredients.set(new_ingredients)

        if validated_data.get('tags'):
            tags_for_recipe = validated_data.pop('tags')
            new_tags = []

            for tag in tags_for_recipe:
                checked_tag = get_object_or_404(Tag, id=tag.id)
                new_tags.append(checked_tag)

            instance.tags.set(new_tags)

        return super().update(instance, validated_data)
