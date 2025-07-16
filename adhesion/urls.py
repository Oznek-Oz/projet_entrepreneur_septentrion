from django.urls import path
from . import views

urlpatterns = [
    path('', views.adhesion, name='adhesion'),
    path('confirmer/<uuid:token>/', views.confirmer_adhesion, name='confirmer'),
]
