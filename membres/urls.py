from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profil/', views.profil, name='profil'),
    path('annuaire/', views.annuaire, name='annuaire'),
    path('publications/', views.publications, name='publications'),
    path('ressources/', views.ressources, name='ressources'),
    path('forum/', views.forum, name='forum'),
]
