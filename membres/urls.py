from django.urls import path
from . import views

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    
]

from django.contrib.auth import views as auth_views

urlpatterns += [
    path('connexion/', auth_views.LoginView.as_view(template_name='membres/connexion.html'), name='connexion'),
    path('deconnexion/', auth_views.LogoutView.as_view(next_page='accueil'), name='deconnexion'),
]