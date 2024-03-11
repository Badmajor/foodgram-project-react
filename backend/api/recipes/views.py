from django_filters import rest_framework as filters
from rest_framework import mixins, viewsets

from api.recipes.permissions import OwnerAndAdminChange
from api.recipes.serializers import IngredientSerializer, RecipeSerializer, TagSerializer
from recipes.models import Ingredient, Recipe, Tag


def check_recipe_data(data: dict) -> bool:
    if not all(data.values()):
        return False

    return True


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.order_by('-pub_date')
    serializer_class = RecipeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('author', 'tags__slug')
    permission_classes = (OwnerAndAdminChange,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return super().update(request, *args, **kwargs)



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
