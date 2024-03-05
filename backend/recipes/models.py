from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    measurement_unit = models.CharField(max_length=10)


class Tag(models.Model):
    title = models.CharField(max_length=10)
    slug = models.CharField(max_length=10)
    color = models.CharField(max_length=10)


class Recipe(models.Model):
    author = models.ForeignKey(
        User, related_name='recipes',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=128)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
    )
    description = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe'
    )
    duration = models.DurationField()


class IngredientRecipe(models.Model):
    ingredients = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE
    )
    quantity = models.PositiveSmallIntegerField(
        default=1
    )


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE
    )
