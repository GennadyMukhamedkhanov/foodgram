from django.urls import path
from api.views.favorites.add_delete import FavoriteCreateDeleteView
from api.views.ingredients.get import IngredientsGetView
from api.views.ingredients.list import IngredientsListView
from api.views.recipes.recipes_get_patch_delete_view import (
    RecipesGetPatchDeleteView
)
from api.views.recipes.recipes_list_add_wiew import RecipesListAddView
from api.views.shopping_list.download_shopping_cart import (
    DownloadShoppingCartView
)
from api.views.shopping_list.shopping_list_add_delete import (
    ShoppingListAddDeleteView
)
from api.views.subscribes.create_delete import SubscribeCreateDeleteView
from api.views.subscribes.list import SubscribeListView
from api.views.tegs.get import TegsGetView
from api.views.tegs.list import TegsListView
from api.views.users.get_token import TokenView
from api.views.users.list_create import UserListCreateView
from api.views.users.logout_token import TokenLogoutView
from api.views.users.personal_profile import PersonalProfileView
from api.views.users.profile_by_id import UserProfileView
from api.views.users.set_password import SetPasswordView

urlpatterns = [
    path('users/', UserListCreateView.as_view()),
    path('users/<int:id>/', UserProfileView.as_view()),
    path('users/me/', PersonalProfileView.as_view()),
    path('users/set_password/', SetPasswordView.as_view()),
    path('users/<int:id>/subscribe/', SubscribeCreateDeleteView.as_view()),
    path('users/subscriptions/', SubscribeListView.as_view()),

    path('auth/token/login/', TokenView.as_view()),
    path('auth/token/logout/', TokenLogoutView.as_view()),

    path('tags/', TegsListView.as_view()),
    path('tags/<int:id>/', TegsGetView.as_view()),

    path('ingredients/', IngredientsListView.as_view()),
    path('ingredients/<int:id>/', IngredientsGetView.as_view()),

    path('recipes/', RecipesListAddView.as_view()),
    path('recipes/<int:id>/', RecipesGetPatchDeleteView.as_view()),
    path('recipes/<int:id>/favorite/', FavoriteCreateDeleteView.as_view()),
    path('recipes/<int:id>/shopping_cart/',
         ShoppingListAddDeleteView.as_view()),
    path('recipes/download_shopping_cart/',
         DownloadShoppingCartView.as_view()),
]
