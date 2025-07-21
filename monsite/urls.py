"""
URL configuration for monsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

from monsite import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accueil.urls")),  # Include the accueil app's URLs
    path("membres/", include("membres.urls")),  # Include the membres app's URLs
    path("adhesion/", include("adhesion.urls")),
    path("blog/", include("blog.urls")),  # Include the blog app's URLs
    path("contact/", include('contact.urls')),
    path("galerie/", include("galerie.urls")),  # Include the galerie app's URLs
    path('newsletter/', include('newsletter.urls')),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)