import django_filters

from recipes.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter(field_name='author__id')
    tags = django_filters.CharFilter(field_name='tags__slug')
    is_in_shopping_cart = django_filters.NumberFilter(field_name='is_in_shopping_cart__id')
    is_favorited = django_filters.NumberFilter(field_name='is_favorited')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_in_shopping_cart', 'is_favorited',)
