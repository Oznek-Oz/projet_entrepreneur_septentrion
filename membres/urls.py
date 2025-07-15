from django.urls import path
from . import views
from .views import forum_list, forum_detail, forum_create, forum_reply, forum_delete

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profil/', views.profil, name='profil'),
    path('annuaire/', views.annuaire, name='annuaire'),
    path('publications/', views.publications, name='publications'),
    path('ressources/', views.ressources, name='ressources'),
    path('forum/', views.forum, name='forum'),
    path('connexion/' , views.connexion, name='connexion'),
    path('forum/', forum_list, name='forum_list'),
    path('forum/nouveau/', forum_create, name='forum_create'),
    path('forum/<int:pk>/', forum_detail, name='forum_detail'),
    path('forum/<int:pk>/repondre/', forum_reply, name='forum_reply'),
    path('forum/<int:pk>/supprimer/', forum_delete, name='forum_delete'),
]
