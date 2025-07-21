from django.urls import path
from . import views
from .views import assistant_publication, forum_list, forum_detail, forum_create, forum_reply, forum_delete, publication_modifier, publication_supprimer
from .views import ressources

urlpatterns = [
    path('assistant-publication/', assistant_publication, name='assistant_publication'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profil/', views.profil, name='profil'),
    path('annuaire/', views.annuaire, name='annuaire'),
    path('publications/', views.publications, name='publications'),
    path('publications/modifier/<int:pk>/', publication_modifier, name='modifier_publication'),
    path('publications/supprimer/<int:pk>/', publication_supprimer, name='supprimer_publication'),
    path('ressources/', ressources, name='ressources'),
    path('connexion/' , views.connexion, name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('forum/', forum_list, name='forum'),
    path('forum/nouveau/', forum_create, name='forum_create'),
    path('forum/<int:pk>/', forum_detail, name='forum_detail'),
    path('forum/<int:pk>/repondre/', forum_reply, name='forum_reply'),
    path('forum/<int:pk>/supprimer/', forum_delete, name='forum_delete'),
    path('messages-publication/', views.messages_publication, name='messages_publication'),
    path('publications/modifier/<int:id>/', views.modifier_publication, name='modifier_publication'),
    path('publications/supprimer/<int:id>/', views.supprimer_publication, name='supprimer_publication'),
    path('publications/supprimer-multiple/', views.supprimer_publications_multiple, name='supprimer_publications_multiple'),
    
]
