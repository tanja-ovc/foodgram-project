from rest_framework import serializers

from recipes.models import Ingredient


class IngredientsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
