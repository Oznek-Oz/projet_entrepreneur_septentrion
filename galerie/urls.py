from django.urls import path
from . import views

urlpatterns = [
    # URL pattern for the gallery page
    path('', views.galerie, name='galerie'),
]