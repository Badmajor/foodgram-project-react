from django.contrib import admin

from . import models


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'display_ingredients', 'cooking_time',
        'pub_date', 'author', 'display_tags', 'display_count_favorites'
    )
    list_filter = ('name', 'author', 'tags',)



    def display_ingredients(self, obj):
        ingredients_list = []
        for ingr in obj.ingredientrecipe_set.all():
            string = f'{ingr.ingredient.name} - {ingr.amount} {ingr.ingredient.measurement_unit}'
            ingredients_list.append(string)
        return ', '.join(ingredients_list)

    def display_tags(self, obj):
        return ', '.join(ingredient.name for ingredient in obj.tags.all())

    def display_count_favorites(self, obj):
        return obj.is_favorited.all().count()


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'color',)
