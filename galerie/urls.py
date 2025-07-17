
# galerie/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.galerie_view, name='galerie'),
    path('origine/<str:origine>/', views.galerie_filtre, name='galerie_filtrée'),
]
