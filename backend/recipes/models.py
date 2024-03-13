from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

LONG_STR = settings.SIZE_LONG_STRING
SHORT_STR = settings.SIZE_SHORT_STRING


class NameFieldStrMethodBaseModel(models.Model):
    name = models.CharField('Название', max_length=LONG_STR, )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Ingredient(NameFieldStrMethodBaseModel):
    measurement_unit = models.CharField('Единица измерения', max_length=SHORT_STR)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'ингредиенты'
        default_related_name = 'ingredient'


class Tag(NameFieldStrMethodBaseModel):
    slug = models.CharField(max_length=SHORT_STR)
    color = models.CharField('Цвет', max_length=SHORT_STR)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'тэги'
        default_related_name = 'tag'


class Recipe(NameFieldStrMethodBaseModel):
    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        default_related_name = 'recipe'

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор рецепта',
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=False,
        blank=False,
        verbose_name='Изображение',
    )
    text = models.TextField('Описание',)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Тэги',
    )
    cooking_time = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        verbose_name='Время приготовления',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )
    is_favorited = models.ManyToManyField(
        User,
        through='UsersRecipesFavorite',
        related_name='favorite recipes',
        verbose_name='Кому понравился рецепт'
    )

    is_in_shopping_cart = models.ManyToManyField(
        User,
        through='ShoppingCart',
        related_name='buy it',
        verbose_name='Кто добавил в список покупок',
    )



class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.PositiveSmallIntegerField()
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('ingredient', 'recipe'),
                                    name='ingredient_recipe_unique'),
        )
    verbose_name = 'Ингредиент'
    verbose_name_plural = 'ингредиенты'


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag, on_delete=models.CASCADE,
        verbose_name='Тэг',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'тэги'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )

    class Meta:
        verbose_name = 'Пользователь хочет купить'
        verbose_name_plural = verbose_name


class UsersRecipesFavorite(ShoppingCart):
    class Meta:
        verbose_name = 'Любимый рецепт пользователя'
        verbose_name_plural = 'любимые рецепты пользователя'
