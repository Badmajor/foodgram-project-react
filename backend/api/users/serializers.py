from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, validators

from recipes.models import Recipe
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


class UserSerializerWithRecipesList(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = (CustomUserSerializer.Meta.fields
                  + ('recipes', 'recipes_count'))

    def get_recipes_count(self, user):
        return Recipe.objects.filter(author=user).count()

    def get_recipes(self, user):
        from api.recipes.serializers import RecipeListForUserSerializer

        limit = self._get_limit_recipe()
        recipes = user.recipe.all()
        if limit:
            recipes = recipes[:limit]
        serializer = RecipeListForUserSerializer(recipes, many=True)
        return serializer.data

    def _get_limit_recipe(self):
        recipes_limit = self.context.get('recipes_limit', False)
        return int(recipes_limit)


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializerWithRecipesList()

    class Meta:
        model = Subscription
        fields = ('user',)

    def to_representation(self, instance):
        return super().to_representation(instance).get('user')
