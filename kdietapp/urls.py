from django.urls import path
from .views import indexPageView
from .views import serumLevelPageView
from .views import trackerPageView
from .views import pricingPageView
from .views import bloghomePageView
from .views import blogpostPageView
from .views import faqPageView
from .views import register_request
from .views import login_request, profile
from .views import logout_request


urlpatterns = [
    path("logout/", logout_request, name="logout"),
    path('login/', login_request, name="login"),
    path('register/', register_request, name="register"),
    path('profile/', profile, name='profile'),

    path('portitem/', faqPageView, name='portitem'),
    path('faq/', faqPageView, name='faq'),
    path('blogpost/', blogpostPageView, name='blogpost'),
    path('bloghome/', bloghomePageView, name='bloghome'),
    path('pricing/', pricingPageView, name='pricing'),

    path('tracker/', trackerPageView, name='tracker'),
    path('serum_levels/', serumLevelPageView, name='serum_levels'),
    path('', indexPageView, name='index'),


]
