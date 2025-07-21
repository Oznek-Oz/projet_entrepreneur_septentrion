"""
Vues pour la gestion de l'adhésion des membres.
- Inscription d'un membre avec envoi d'un email de confirmation personnalisé.
- Validation de l'adhésion via un lien unique reçu par email.
"""
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from membres.models import Membres  # <-- importer le modèle
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
import uuid
from django.views.decorators.http import require_GET
from django.http import JsonResponse


def adhesion(request):
    """
    Vue permettant à un utilisateur de s'inscrire comme membre.
    - Vérifie la correspondance des mots de passe.
    - Vérifie l'unicité de l'email.
    - Crée un membre avec un token de confirmation unique.
    - Envoie un email de confirmation avec un lien personnalisé.
    """
    # Si 
    if request.user.is_authenticated:
        return redirect('dashboard')

    # Si l'utilisateur est déjà connecté, on le redirige vers la page d'adhésion
    if request.method == 'POST':
        # Validation côté serveur
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')
        nom = request.POST.get('nom', '').strip()
        prenom = request.POST.get('prenom', '').strip()
        
        # Validation des champs obligatoires
        if not username or len(username) < 3:
            messages.error(request, "Le nom d'utilisateur doit contenir au moins 3 caractères.")
            return redirect('adhesion')
            
        if not email:
            messages.error(request, "L'email est obligatoire.")
            return redirect('adhesion')
            
        # Validation du format email
        import re
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            messages.error(request, "Format d'email invalide.")
            return redirect('adhesion')
            
        if not password:
            messages.error(request, "Le mot de passe est obligatoire.")
            return redirect('adhesion')
            
        if len(password) < 6:
            messages.error(request, "Le mot de passe doit contenir au moins 6 caractères.")
            return redirect('adhesion')
            
        if password != confirm:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('adhesion')
            
        if not nom:
            messages.error(request, "Le nom est obligatoire.")
            return redirect('adhesion')
            
        if not prenom:
            messages.error(request, "Le prénom est obligatoire.")
            return redirect('adhesion')

        # Vérification de l'unicité de l'email et du nom d'utilisateur
        if Membres.objects.filter(email=email).exists():
            messages.error(request, "Un compte existe déjà avec cet email.")
            return redirect('adhesion')
            
        if Membres.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return redirect('adhesion')

        membres = Membres(
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
            photo=request.FILES.get('photo'),
            confirmation_token=str(uuid.uuid4())  # Ajout du token
        )
        membres.save()
        # Envoi de l'email de confirmation
        confirmation_url = request.build_absolute_uri(reverse('confirmer', args=[membres.confirmation_token]))
        sujet = "Confirmation de votre adhésion à la communauté"
        message = f"Bonjour {membres.prenom or membres.nom},\n\nMerci pour votre demande d'adhésion. Veuillez confirmer votre inscription en cliquant sur le lien suivant :\n{confirmation_url}\n\nBienvenue parmi nous !"
        send_mail(
            sujet,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [membres.email],
            fail_silently=False,
        )
        messages.success(request, "Inscription réussie. Un email de confirmation vous a été envoyé.")
        login(request, membres)
        return redirect('dashboard')
    return render(request, 'adhesion/adhesion.html')


def confirmer_adhesion(request, token):
    """
    Vue appelée lors du clic sur le lien de confirmation reçu par email.
    - Valide l'adhésion du membre si le token est correct.
    - Affiche un message de succès ou d'erreur.
    """
    try:
        membres = Membres.objects.get(confirmation_token=token)
        membres.is_confirmed = True
        membres.save()
        return HttpResponse("Votre adhésion est confirmée. Merci et bienvenue !")
    except Membres.DoesNotExist:
        return HttpResponse("Lien invalide ou déjà utilisé.")


@require_GET
def check_username(request):
    username = request.GET.get('username', '').strip()
    exists = Membres.objects.filter(username=username).exists()
    return JsonResponse({'available': not exists})
