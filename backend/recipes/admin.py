from django.contrib import admin

from recipes.models.favourite.models import Favourite
from recipes.models.ingredient.models import Ingredient
from recipes.models.recipe.models import Recipe, IngredientWithAmount
from recipes.models.shopping_list.models import ShoppingList
from recipes.models.subscriptions.models import Subscription
from recipes.models.tag.models import Tag
from users.models import User


@admin.register(Tag)
class TegAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
# Todo --------------------------------------------
#
# class NewIngredientInline(admin.TabularInline):
#     model = IngredientWithAmount
#     extra = 1

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    #inlines = [NewIngredientInline,]

# Todo --------------------------------------------

# class SubscriptionInline(admin.TabularInline):
#     model = Subscription
#     extra = 1


class IngredientInline(admin.TabularInline):
    model = IngredientWithAmount
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [IngredientInline, ]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass


@admin.register(Favourite)
class FavouriteRecipeAdmin(admin.ModelAdmin):
    pass


#class

@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    pass


@admin.register(IngredientWithAmount)
class IngredientWithAmountListAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')

