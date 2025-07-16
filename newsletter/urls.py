from django.urls import path
from .views import inscription_newsletter

urlpatterns = [
    path('subscribe/', inscription_newsletter, name='inscription_newsletter'),
]
