from django.contrib.auth import get_user_model
from django.db.models import Count
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from ..paginators import CustomPageNumberPagination
from ..serializers import UserSerializerForSubscriptions

User = get_user_model()


class PaginatedUserViewSet(UserViewSet):
    pagination_class = CustomPageNumberPagination

    @action(detail=False,
            methods=['get'],
            serializer_class=UserSerializerForSubscriptions,
            permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request, *args, **kwargs):
        """
        Lists the subscriptions of a current user.
        Requests are to be sent at /users/subscriptions/.
        """
        def get_queryset(self):
            return User.objects.filter(
                subscriptions_to_the_user=self.request.user
            ).annotate(
                recipes_count=Count('recipes')
            )
        queryset = get_queryset(self)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True,
            methods=['post', 'delete'],
            queryset=User.objects.all(),
            serializer_class=UserSerializerForSubscriptions,
            permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, *args, **kwargs):
        """
        Subscribes/unsubscribes a user to/from another user.
        Requests are to be sent at /users/<id>/subscribe/.
        """
        user_id = self.kwargs['id']
        user = get_object_or_404(User, id=user_id)

        if request.method == 'POST':
            if request.user in user.subscriptions_to_the_user.all():
                return Response(
                    {'detail': 'Вы уже подписаны на данного пользователя.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if request.user == user:
                return Response(
                    {'detail': 'Подписка на самого себя невозможна.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.subscriptions_to_the_user.add(request.user)

        if request.method == 'DELETE':
            if request.user not in user.subscriptions_to_the_user.all():
                return Response(
                    {'detail': 'Вы не подписаны на данного пользователя.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            user.subscriptions_to_the_user.remove(request.user)
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if request.method == 'POST':
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED,
                            headers=headers)
        if request.method == 'DELETE':
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
