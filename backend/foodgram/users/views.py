from api.serializers import (
    SubscriptionSerializer,
    UserSerializer,
    UserSubSerializer,
)
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Subscription, User


class UserViewSet(UserViewSet):
    serializer_class = UserSerializer

    @action(methods=['get'], detail=False)
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(methods=['get'], detail=False)
    def subscriptions(self, request):
        queryset = User.objects.filter(subscription__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(methods=['post', 'delete'], detail=True)
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = UserSubSerializer(
                data={'user': user.id, 'author': author.id},
                context={'request': request},
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        try:
            Subscription.objects.get(user=user, author=author).delete()
        except Exception:
            return Response(
                {'detail': 'Ошибка отписки'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
