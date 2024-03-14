from djoser.views import UserViewSet
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.users.serializers import UserSerializerWithRecipesList
from users.models import Subscription

from .serializers import SubscriptionSerializer


class SubscriptionViewSet(mixins.ListModelMixin,
                          viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Subscription.objects.filter(subscriber=user)
        limit = self.request.query_params.get('limit', False)
        if limit:
            queryset = queryset[:int(limit)]
        return queryset

    def get_serializer_context(self):
        context = self.request.query_params
        return context


class UserViewSetWithActions(UserViewSet):

    @action(["get", "put", "patch", "delete"],
            detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        return super().me(request, *args, **kwargs)

    @action(["post", "delete"], detail=True)
    def subscribe(self, request, *args, **kwargs):
        user = self.get_object()
        subscriber = request.user
        sub_exist = Subscription.objects.filter(
            user=user, subscriber=subscriber
        ).exists()
        if user == subscriber:
            return Response('It is not possible to subscribe to yourself',
                            status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'POST':
            if sub_exist:
                return Response('Subscription exist',
                                status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.create(user=user, subscriber=subscriber)
            serializer = UserSerializerWithRecipesList(
                user, context=request.query_params
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not sub_exist:
                return Response('Subscription not exist',
                                status=status.HTTP_400_BAD_REQUEST)
            Subscription.objects.get(user=user, subscriber=subscriber).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
