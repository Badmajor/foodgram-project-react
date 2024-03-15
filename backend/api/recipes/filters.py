import django_filters

from recipes.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    author = django_filters.NumberFilter(field_name='author__id')
    tags = django_filters.CharFilter(field_name='tags__slug')
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_user_in_queryset')
    is_favorited = django_filters.NumberFilter(
        method='filter_user_in_queryset')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_in_shopping_cart', 'is_favorited',)

    def filter_user_in_queryset(self, queryset, name, value):
        user = self.request.user
        if value and user.is_authenticated:
            data = {name: user}
            queryset = queryset.filter(**data)
        return queryset
