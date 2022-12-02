from django.urls import path
from .views import indexPageView
from .views import serumLevelPageView
from .views import trackerPageView
from .views import suggestionsPageView
from .views import bloghomePageView
from .views import blogpostPageView
from .views import register_request
from .views import login_request, profile
from .views import logout_request
from .views import addProfilePageView
from .views import editProfilePageView
from .views import addFoodPageView
from .views import deleteFoodPageView
from .views import showFoodPageView
from .views import editFoodPageView
from .views import importNutrientsPageView

urlpatterns = [
    path("logout/", logout_request, name="logout"),
    path('login/', login_request, name="login"),
    path('register/', register_request, name="register"),
    path('profile/', profile, name='profile'),

    path('blogpost/', blogpostPageView, name='blogpost'),
    path('bloghome/', bloghomePageView, name='bloghome'),
    path('suggestions/', suggestionsPageView, name='suggestions'),

    path('editFood/', editFoodPageView, name='editFood'),
    path('showFood/', showFoodPageView, name='showFood'),
    path('tracker/', trackerPageView, name='tracker'),
    path('addFood/', addFoodPageView, name='addFood'),
    path('serum_levels/', serumLevelPageView, name='serum_levels'),
    path('addProfile/', addProfilePageView, name='addProfile'),
    path('editProfile/', editProfilePageView, name='editProfile'),
    path('deleteFood/', deleteFoodPageView, name='deleteFood'),
    path('importNutrients/', importNutrientsPageView, name='importNutrients'),
    path('', indexPageView, name='index'),



]
