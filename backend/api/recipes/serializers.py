import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers

from api.users.serializers import CustomUserSerializer
from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('color', 'name', 'slug')

    def to_internal_value(self, data):
        if isinstance(data, int):
            data = {'id': data}
        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Ingredient
        fields = ('id', 'measurement_unit', 'name',)
        read_only_fields = ('measurement_unit', 'name',)


class IngredientRecipeSerializer(serializers.ModelSerializer):
    measurement_unit = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit

    def get_name(self, obj):
        return obj.ingredient.name


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True, allow_null=True)
    ingredients = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=True,
        allow_empty=False,
    )
    tags = TagSerializer(many=True, required=True, allow_empty=False)
    author = CustomUserSerializer(read_only=True)
    cooking_time = serializers.IntegerField(allow_null=False)

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags',
                  'image', 'name', 'text',
                  'cooking_time', 'author',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self._add_ingredientrecipe(ingredients_data, recipe)
        self._add_tagrecipe(tags_data, recipe)

        return recipe

    def to_representation(self, instance):
        user = self.context['request'].user
        representation = super().to_representation(instance)
        ingredients = []
        for ingredient_obj in IngredientRecipe.objects.filter(recipe=instance):
            ingredient = IngredientRecipeSerializer(ingredient_obj)
            ingredients.append(ingredient.to_representation(ingredient_obj))

        representation['ingredients'] = ingredients
        representation['is_favorited'] = user in instance.is_favorited.all()
        representation['is_in_shopping_cart'] = (
                user in instance.is_in_shopping_cart.all())
        return representation

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        self._add_ingredientrecipe(ingredients_data, instance)
        self._add_tagrecipe(tags_data, instance)

        return super().update(instance, validated_data)

    def validate_ingredients(self, ingredients):
        if len(ingredients) != len(set(i.get('id') for i in ingredients)):
            raise serializers.ValidationError(
                'ingredients should not be repeated')
        for ingredient_data in ingredients:
            if not Ingredient.objects.filter(
                    pk=ingredient_data.get('id')).exists():
                raise serializers.ValidationError('Ingredient Does Not Exist')
            if not ingredient_data.get('amount'):
                raise serializers.ValidationError('amount most be positive')
        return ingredients

    def validate_tags(self, tags):
        if len(tags) != len(set(i.get('id') for i in tags)):
            raise serializers.ValidationError('tags should not be repeated')
        for tag in tags:
            if not Tag.objects.filter(pk=tag.get('id')):
                raise serializers.ValidationError('Tag Does Not Exist')
        return tags

    def validate_cooking_time(self, attrs):
        if attrs:
            return attrs
        raise serializers.ValidationError('cooking_time most be positive')

    def _add_ingredientrecipe(
            self, ingredients: list, instance: Recipe
    ) -> None:
        created_ingredientrecipe = []
        IngredientRecipe.objects.filter(recipe=instance).delete()
        for ingredient_data in ingredients:
            ingredient = Ingredient.objects.get(pk=ingredient_data.get('id'))
            amount = ingredient_data.get('amount')
            ingredient_recipe = IngredientRecipe(
                ingredient=ingredient,
                recipe=instance,
                amount=amount,
            )
            created_ingredientrecipe.append(ingredient_recipe)
        IngredientRecipe.objects.bulk_create(created_ingredientrecipe)

    def _add_tagrecipe(self, tags: list, instance: Recipe) -> None:
        instance.tags.clear()
        for tag in tags:
            tag = Tag.objects.get(pk=tag.get('id'))
            instance.tags.add(tag)


class RecipeListForUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
