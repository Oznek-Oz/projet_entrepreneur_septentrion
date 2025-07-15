from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from membres.models import Membre  # <-- importer le modèle

def adhesion(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('adhesion')

        email = request.POST.get('email')
        if Membre.objects.filter(email=email).exists():
            messages.error(request, "Un compte existe déjà avec cet email.")
            return redirect('adhesion')

        membre = Membre(
            username=request.POST.get('username'),
            nom=request.POST.get('nom'),
            prenom=request.POST.get('prenom'),
            email=email,
            password=make_password(password),
            ville=request.POST.get('ville'),
            profession=request.POST.get('profession'),
            statut=request.POST.get('statut'),
            mini_cv=request.POST.get('mini_cv'),
            facebook=request.POST.get('facebook'),
            linkedin=request.POST.get('linkedin'),
            twitter=request.POST.get('twitter'),
            type_adhesion=request.POST.get('type_adhesion'),
            date_adhesion=request.POST.get('date_adhesion'),
            montant=request.POST.get('montant') or 0,
            moyen_paiement=request.POST.get('moyen_paiement'),
            numero_transaction=request.POST.get('numero_transaction'),
            photo=request.FILES.get('photo')
        )
        membre.save()
        messages.success(request, "Inscription réussie. Bienvenue !")
        return redirect('dashboard')  # À adapter selon ta route

    return render(request, 'adhesion/adhesion.html')
