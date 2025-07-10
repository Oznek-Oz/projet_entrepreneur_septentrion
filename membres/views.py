from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def dashboard(request):
    return render(request, 'membres/dashboard.html')


def profil(request):
    return render(request, 'membres/profil.html')

def annuaire(request):
    return render(request, 'membres/annuaire.html')

def publications(request):
    return render(request, 'membres/publications.html')

def ressources(request):
    return render(request, 'membres/ressources.html')

def forum(request):
    return render(request, 'membres/forum.html')
