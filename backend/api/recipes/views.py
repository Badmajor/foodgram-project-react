import io

from django.db.models import F, Sum
from django_filters import rest_framework as filters
from django.http import FileResponse, response
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework import mixins, viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from api.recipes.permissions import OwnerAndAdminChange
from api.recipes.serializers import (IngredientSerializer,
                                     RecipeListForUserSerializer,
                                     RecipeSerializer,
                                     TagSerializer,)
from recipes.models import (Ingredient,
                            IngredientRecipe,
                            Recipe,
                            ShoppingCart,
                            Tag,
                            UsersRecipesFavorite,)

def create_pdf(data_list):

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
        user = request.user
        if request.method == 'POST':
            try:
                recipe = self.get_object()
            except response.Http404:
                return Response('Recipe is not exist', status=status.HTTP_400_BAD_REQUEST)
        else:
            recipe = self.get_object()
        serializer = RecipeListForUserSerializer(recipe)
        if request.method == 'POST':
            _, created = ShoppingCart.objects.get_or_create(user=user, recipe=recipe)
            if created:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response('Recipe already in your shopping cart', status=status.HTTP_400_BAD_REQUEST)
        try:
            cart = get_object_or_404(ShoppingCart, user=user, recipe=recipe)
        except response.Http404:
            return Response('Recipe is not in ShoppingCart', status=status.HTTP_400_BAD_REQUEST)
        cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
        if request.method == 'POST':
            try:
                recipe = self.get_object()
            except response.Http404:
                return Response('Recipe is not exist', status=status.HTTP_400_BAD_REQUEST)
        else:
            recipe = self.get_object()
        user = request.user
        serializer = RecipeListForUserSerializer(recipe)
        if request.method == 'POST':
            _, created = UsersRecipesFavorite.objects.get_or_create(user=user, recipe=recipe)
            if created:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response('Recipe already in your favorite list', status=status.HTTP_400_BAD_REQUEST)
        try:
            favorite = get_object_or_404(UsersRecipesFavorite, user=user, recipe=recipe)
        except response.Http404:
            return Response('Recipe is not in ShoppingCart', status=status.HTTP_400_BAD_REQUEST)
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


