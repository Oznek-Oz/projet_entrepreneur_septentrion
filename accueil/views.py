from membres.models import Membres
def promoteurs(request):
    promoteurs = Membres.objects.filter(is_promoteur=True, is_actif=True)
    return render(request, 'accueil/promoteurs.html', {'promoteurs': promoteurs})
from django.shortcuts import render
from don.forms import DonForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def accueil(request):
    """
    Render the home page.
    """
    from membres.models import Publication, Membres
    publications = Publication.objects.filter(valide=True).order_by('-date_publication')[:3]
    promoteurs = Membres.objects.filter(is_promoteur=True, is_actif=True)
    return render(request, 'accueil/index.html', {'publications': publications, 'promoteurs': promoteurs})

def a_propos(request):
    """
    Render the 'about' page.
    """
    return render(request, 'accueil/a_propos.html')

def contact(request):
    """
    Render the 'contact' page.
    """
    return render(request, 'accueil/contact.html')
