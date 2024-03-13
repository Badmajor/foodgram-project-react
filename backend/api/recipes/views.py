import io

from django.db.models import F, Sum
from django_filters import rest_framework as filters
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework import mixins, viewsets, permissions, status, exceptions
from rest_framework.decorators import action
from rest_framework.response import Response

from api.recipes.permissions import OwnerAndAdminChange
from api.recipes.serializers import (IngredientSerializer,
                                     RecipeListForUserSerializer,
                                     RecipeSerializer,
                                     TagSerializer, )
from recipes.models import (Ingredient,
                            IngredientRecipe,
                            Recipe,
                            ShoppingCart,
                            Tag,
                            UsersRecipesFavorite, )


def create_pdf(data_list: list[str]):
    buffer = io.BytesIO()
    file = canvas.Canvas(buffer, pagesize=letter)
    y = 750
    for row in data_list:
        file.drawString(100, 750, str(row))
        y -= 30
    file.save()
    pdf_file = buffer.getvalue()
    buffer.close()
    return pdf_file


def _get_obj_or_400(klass, **kwargs):
    if hasattr(klass, "_default_manager"):
        queryset = klass._default_manager.all()
    try:
        return queryset.get(**kwargs)
    except Exception:
        raise exceptions.ValidationError(detail=f'{klass.__name__} not exist')


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.order_by('-pub_date')
    serializer_class = RecipeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('author', 'tags__slug', 'is_in_shopping_cart', 'is_favorited')
    permission_classes = (OwnerAndAdminChange,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return super().update(request, *args, **kwargs)

    @action(["post", "delete"],
            permission_classes=(permissions.IsAuthenticated,),
            detail=True)
    def shopping_cart(self, request, *args, **kwargs):
        return self.__base_action_method(ShoppingCart, request, *args, **kwargs)


    @action(["get"],
            permission_classes=(permissions.IsAuthenticated,),
            detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        ingredients = ShoppingCart.objects.filter(
            user=request.user
        ).values(
            name=F('recipe__ingredients__name')
        ).annotate(amount=Sum(
            'recipe__ingredients__ingredientrecipe__amount'))
        file = create_pdf(ingredients)
        return FileResponse(filename=file,
                            status=status.HTTP_200_OK,
                            content_type='application/pdf')

    @action(['post', 'delete'],
            permission_classes=(permissions.IsAuthenticated,),
            detail=True)
    def favorite(self, request, *args, **kwargs):
        return self.__base_action_method(UsersRecipesFavorite, request, *args, **kwargs)

    def _get_recipe_or_400(self):
        try:
            recipe = self.get_object()
            return recipe
        except Exception:
            raise exceptions.ValidationError(detail='Recipe not exist')

    def __base_action_method(self, klass, request, *args, **kwargs) -> Response:
        """Return Response depending on the state of the objects."""
        method = request.method
        user = request.user
        if method == 'POST':
            recipe = self._get_recipe_or_400()
            serializer = RecipeListForUserSerializer(recipe)
            _, created = klass.objects.get_or_create(user=user, recipe=recipe)
            if created:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response('Recipe already in list', status=status.HTTP_400_BAD_REQUEST)
        if method == 'DELETE':
            recipe = self.get_object()
            favorite = _get_obj_or_400(klass, user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


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
