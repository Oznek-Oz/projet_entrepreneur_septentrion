from django.urls import path
from . import views
from .views import promoteurs

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('about/', views.a_propos, name='about'),
    path('promoteurs/', promoteurs, name='promoteurs'),
]
