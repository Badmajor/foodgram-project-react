from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, validators
from rest_framework.exceptions import AuthenticationFailed

from users.models import Subscription

User = get_user_model()


class MetaAllUserFieldsMixin:
    """
    Adding class Meta with fields = 'username', 'email',
    'first_name', 'last_name', 'password'.
    """
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'id',
            'first_name',
            'last_name',
            'password',
        )
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'email': {'required': True},
            'password': {'write_only': True},
        }


class CustomUserCreateSerializer(MetaAllUserFieldsMixin, UserCreateSerializer):
    email = serializers.EmailField(
        validators=[
            validators.UniqueValidator(
                User.objects.all()
            )
        ]
    )


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(MetaAllUserFieldsMixin.Meta):
        fields = MetaAllUserFieldsMixin.Meta.fields + ('is_subscribed',)

    def get_is_subscribed(self, obj):
        return Subscription.objects.filter(user=obj).exists()

    @property
    def data(self):
        request = self.context['request']
        if (request.path == '/api/users/me/'
                and not request.user.is_authenticated):
            raise AuthenticationFailed()
        return super().data
