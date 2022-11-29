from django.urls import path
from .views import indexPageView
from .views import serumLevelPageView
from .views import contactPageView
from .views import pricingPageView
from .views import bloghomePageView
from .views import blogpostPageView
from .views import faqPageView
from .views import portitemPageView
from .views import portoverviewPageView
from .views import register_request
from .views import login_request
from .views import serumLevelPageView

urlpatterns = [
    path('login', login_request, name="login"),
    path('register/', register_request, name="register"),
    path('portoverview/', portitemPageView, name='portitem'),
    path('portoverview/', portoverviewPageView, name='portoverview'),
    path('portitem/', faqPageView, name='portitem'),
    path('faq/', faqPageView, name='faq'),
    path('blogpost/', blogpostPageView, name='blogpost'),
    path('bloghome/', bloghomePageView, name='bloghome'),
    path('pricing/', pricingPageView, name='pricing'),
    path('contact/', contactPageView, name='contact'),
    path('serum_levels/', serumLevelPageView, name='serum_levels'),
    path('', indexPageView, name='index'),

]
