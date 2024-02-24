from django.urls import path

from api.views.favorites.views import FavoriteView
from api.views.ingredients.views import IngredientsListView, IngredientsGetView
from api.views.recipes.views import RecipesListAddView, RecipesGetPatchDeleteView
from api.views.shopping_list.views import ShoppingListAddDeleteView, \
    DownloadShoppingCartView
from api.views.subscribes.views import SubscribeListView, \
    SubscribeCreateDeleteView
from api.views.tegs.views import TegsListView, TegsGetView
from api.views.users.views import (UserListCreateView, UserProfileView,
                                   TokenView, TokenLogoutView,
                                   PersonalProfileView, SetPasswordView)

# GGG 111
urlpatterns = [
    # Users
    path('users/', UserListCreateView.as_view()),
    path('users/<int:id>/', UserProfileView.as_view()),
    path('users/me/', PersonalProfileView.as_view()),
    path('users/set_password/', SetPasswordView.as_view()),
    path('auth/token/login/', TokenView.as_view()),
    path('auth/token/logout/', TokenLogoutView.as_view()),
    # Tegs
    path('tags/', TegsListView.as_view()),
    path('tags/<int:id>/', TegsGetView.as_view()),
    # Ingredients
    path('ingredients/', IngredientsListView.as_view()),
    path('ingredients/<int:id>/', IngredientsGetView.as_view()),
    # Subscribe
    path('users/<int:id>/subscribe/', SubscribeCreateDeleteView.as_view()),
    path('users/subscriptions/', SubscribeListView.as_view()),
    # Favorite
    path('recipes/<int:id>/favorite/', FavoriteView.as_view()),
    # Shopping list
    path('recipes/<int:id>/shopping_cart/',
         ShoppingListAddDeleteView.as_view()),
    path('recipes/download_shopping_cart/',
         DownloadShoppingCartView.as_view()),
    # Recipes
    path('recipes/', RecipesListAddView.as_view()),
    path('recipes/<int:id>/', RecipesGetPatchDeleteView.as_view()),

]
