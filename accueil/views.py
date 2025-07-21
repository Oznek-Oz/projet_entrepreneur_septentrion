from django.shortcuts import render
from don.forms import DonForm
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
