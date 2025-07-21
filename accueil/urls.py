from django.urls import path
from . import views
from .views import promoteurs

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('about/', views.a_propos, name='about'),
    path('don/', views.don, name='don'),
    path('promoteurs/', promoteurs, name='promoteurs'),
]
