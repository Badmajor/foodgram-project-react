from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=128)
    measurement_unit = models.CharField(max_length=10)


class Tag(models.Model):
    name = models.CharField(max_length=10)
    slug = models.CharField(max_length=10)
    color = models.CharField(max_length=10)


class Recipe(models.Model):
    author = models.ForeignKey(
        User, related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=128)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe'
    )
    cooking_time = models.PositiveSmallIntegerField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    users_who_like_it = models.ManyToManyField(
        User,
        through='UsersRecipesFavorite'
    )
    def is_favorited(self, user):
        return user in self.users_who_like_it.all()


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField()
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
    )


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE
    )


class UsersRecipesFavorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)