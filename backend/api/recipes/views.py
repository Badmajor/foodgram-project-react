from django_filters import rest_framework as filters
from rest_framework import mixins, permissions, viewsets

from api.recipes.serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from recipes.models import Ingredient, Recipe, Tag


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.order_by('-pub_date')
    serializer_class = RecipeSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('name',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(mixins.RetrieveModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.order_by('name')
    serializer_class = IngredientSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('name',)
    pagination_class = None


class TagViewSet(mixins.RetrieveModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.order_by('id')
    serializer_class = TagSerializer
    pagination_class = None
