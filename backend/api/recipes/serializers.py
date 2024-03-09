import base64
from collections import OrderedDict

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, TagRecipe

from api.users.serializers import CustomUserSerializer

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
    image = Base64ImageField(required=False, allow_null=True)
    ingredients = serializers.ListField(
        child=serializers.DictField(),
        write_only=True)
    tags = TagSerializer(many=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'ingredients', 'tags', 'image', 'name', 'text', 'cooking_time', 'author',)
        read_only_fields = ('tags', 'id')

    def create(self, validated_data):
        print(validated_data)
        ingredients_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            ingredient = Ingredient.objects.get(pk=ingredient_data.get('id'))
            amount = ingredient_data.get('amount')
            IngredientRecipe.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=amount,
            )
        for tag in tags_data:
            tag = Tag.objects.get(pk=tag.get('id'))
            TagRecipe.objects.create(
                tag=tag,
                recipe=recipe
            )
        return recipe

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        ingredients = []
        for ingredient_obj in IngredientRecipe.objects.filter(recipe=instance):
            ingredient = IngredientRecipeSerializer(ingredient_obj)
            ingredients.append(ingredient.to_representation(ingredient_obj))
        representation['ingredients'] = ingredients
        representation['is_favorited'] = instance.is_favorited(
            self.context['request'].user)
        representation['is_in_shopping_cart'] = False
        return representation
