import io

from django.db.models import F, Sum
from django.http import FileResponse
from django_filters import rest_framework as filters
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas
from rest_framework import exceptions, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.recipes.permissions import OwnerAndAdminChange
from api.recipes.serializers import (IngredientSerializer,
                                     RecipeListForUserSerializer,
                                     RecipeSerializer, TagSerializer)
from recipes.models import (Ingredient, Recipe, ShoppingCart, Tag,
                            UsersRecipesFavorite)

from .filters import RecipeFilter
from .paginators import RecipePaginator


def create_pdf(data_list: list[str]):
    buffer = io.BytesIO()
    file = canvas.Canvas(buffer)
    pdfmetrics.registerFont(
        ttfonts.TTFont(
            'DejaVu',
            'fonts/DejaVuSerifCondensed.ttf',
        )
    )
    file.setFont("DejaVu", 15)
    y = 750
    for item in data_list:
        row = f'- {item["name"]} - {item["amount"]} {item["unit"]}'
        file.drawString(100, y, row)
        y -= 30
    file.showPage()
    file.save()
    buffer.seek(0)
    return buffer


def _get_obj_or_400(klass, **kwargs):
    if hasattr(klass, "_default_manager"):
        queryset = klass._default_manager.all()
    try:
        return queryset.get(**kwargs)
    except Exception:
        raise exceptions.ValidationError(detail=f'{klass.__name__} not exist')


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (OwnerAndAdminChange,)
    pagination_class = RecipePaginator

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = False
        return super().update(request, *args, **kwargs)

    @action(["post", "delete"],
            permission_classes=(permissions.IsAuthenticated,),
            detail=True)
    def shopping_cart(self, request, *args, **kwargs):
        return self.__base_action_method(
            ShoppingCart, request, *args, **kwargs
        )

    @action(["get"],
            permission_classes=(permissions.IsAuthenticated,),
            detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        ingredients = ShoppingCart.objects.filter(
            user=request.user
        ).values(
            name=F('recipe__ingredients__name'),
            unit=F('recipe__ingredients__measurement_unit')
        ).annotate(amount=Sum(
            'recipe__ingredients__ingredientrecipe__amount'))
        file = create_pdf(ingredients)
        return FileResponse(
            file,
            filename='shopping_cart.pdf',
            status=status.HTTP_200_OK,
            as_attachment=True,)


    @action(['post', 'delete'],
            permission_classes=(permissions.IsAuthenticated,),
            detail=True)
    def favorite(self, request, *args, **kwargs):
        return self.__base_action_method(
            UsersRecipesFavorite, request, *args, **kwargs)

    def _get_recipe_or_400(self):
        try:
            recipe = self.get_object()
            return recipe
        except Exception:
            raise exceptions.ValidationError(detail='Recipe not exist')

    def __base_action_method(
            self, klass, request, *args, **kwargs
    ) -> Response:
        """Return Response depending on the state of the objects."""
        method = request.method
        user = request.user
        if method == 'POST':
            recipe = self._get_recipe_or_400()
            serializer = RecipeListForUserSerializer(recipe)
            _, created = klass.objects.get_or_create(user=user, recipe=recipe)
            if created:
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                'Recipe already in list',
                status=status.HTTP_400_BAD_REQUEST
            )
        if method == 'DELETE':
            recipe = self.get_object()
            print('CheckPoint123', recipe.author, user, klass)
            favorite = _get_obj_or_400(klass, user=user, recipe=recipe)
            print('fdskjfsdfsd', recipe.author, user, klass)
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
