from django.contrib import admin

from .models import Ingredient, IngredientForRecipe, Recipe


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('measurement_unit',)
    search_fields = ('name',)


class IngredientForRecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'id')
    list_filter = ('tags', 'author',)
    search_fields = ('name',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(IngredientForRecipe, IngredientForRecipeAdmin)
