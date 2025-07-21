from django.urls import path
from . import views
from .views import check_username

urlpatterns = [
    path('', views.adhesion, name='adhesion'),
    path('confirmer/<uuid:token>/', views.confirmer_adhesion, name='confirmer'),
    path('check-username/', check_username, name='check_username'),
]
