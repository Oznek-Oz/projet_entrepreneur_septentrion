from django.shortcuts import render
from .forms import DonForm
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def accueil(request):
    """
    Render the home page.
    """
    return render(request, 'accueil/index.html')

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

def don(request):
    """
    Vue pour gérer le formulaire de don et simuler le paiement.
    """
    if request.method == 'POST':
        form = DonForm(request.POST)
        if form.is_valid():
            don = form.save(commit=False)
            # Simulation du paiement : on considère que le paiement est toujours réussi
            don.statut = 'payé'  # À adapter selon votre modèle
            don.save()
            return render(request, 'accueil/don_success.html', {'don': don})
    else:
        form = DonForm()
    return render(request, 'accueil/don_form.html', {'form': form})
