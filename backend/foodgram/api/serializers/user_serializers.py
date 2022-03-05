from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .recipe_lite_serializer import RecipeSerializerLite

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed')

    def get_is_subscribed(self, obj) -> bool:
        current_user = self.context['request'].user
        if current_user.is_authenticated:
            if obj.subscriptions_to_the_user.filter(id=current_user.id):
                return True
        return False


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'password')


class UserSerializerForSubscriptions(CustomUserSerializer):
    recipes = RecipeSerializerLite(many=True, read_only=True)
    recipes_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('email', 'username', 'first_name', 'last_name',)
