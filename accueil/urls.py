from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for the home page
    path('', views.home, name='home'),
]