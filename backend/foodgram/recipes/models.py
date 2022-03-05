from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from tags.models import Tag

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        max_length=70, verbose_name='название', db_index=True
    )
    measurement_unit = models.CharField(
        max_length=10, verbose_name='единица измерения'
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return self.name


class IngredientForRecipe(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        verbose_name='количество', validators=[MinValueValidator(
                1, 'Количество ингредиента не может быть меньше 1')]
    )

    class Meta:
        verbose_name = 'ингредиент для рецепта'
        verbose_name_plural = 'ингредиенты для рецептов'

    def __str__(self):
        return self.ingredient.name


class Recipe(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='название', db_index=True
    )
    image = models.ImageField(verbose_name='изображение')
    text = models.TextField(verbose_name='описание')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='время приготовления в минутах',
        validators=[MinValueValidator(
                1, 'Время приготовления не может быть меньше 1 минуты')]
    )
    ingredients = models.ManyToManyField(
        Ingredient, through=IngredientForRecipe,
        verbose_name='ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='тэги'
    )
    author = models.ForeignKey(
        User, related_name='recipes', verbose_name='автор',
        on_delete=models.CASCADE
    )
    is_favorited = models.BooleanField(
        verbose_name='в вашем избранном',
        default=False
    )
    is_in_shopping_cart = models.BooleanField(
        verbose_name='в вашем списке покупок',
        default=False
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name
