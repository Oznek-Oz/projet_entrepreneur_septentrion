from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for the home page
    path('', views.accueil, name='accueil'),
    path('about/', views.a_propos, name='about'),
    path('don/', views.don, name='don'),
]