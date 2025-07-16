"""
Vues pour la gestion de la newsletter.
- Inscription d'un utilisateur à la newsletter.
- Envoi d'un email de remerciement personnalisé après inscription.
"""

from django.contrib import messages
from django.shortcuts import redirect
from .models import NewsletterSubscriber
from django.core.mail import send_mail
from django.utils.translation import gettext as _
from django.conf import settings

def inscription_newsletter(request):
    """
    Vue permettant à un utilisateur de s'inscrire à la newsletter.
    - Vérifie si l'email est déjà inscrit.
    - Ajoute l'email à la base si nouveau.
    - Envoie un email de remerciement personnalisé.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        # On pourrait aussi récupérer le nom/prénom si le formulaire les propose
        # nom = request.POST.get('nom', '')
        # prenom = request.POST.get('prenom', '')
        if email:
            # Vérifie si l'email existe déjà dans la base
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                NewsletterSubscriber.objects.create(email=email)
                # Prépare le contenu de l'email de remerciement
                sujet = "Merci pour votre inscription à la newsletter !"
                message = f"Bonjour,\n\nMerci de vous être inscrit à notre newsletter. Vous serez informé des nouveautés et actualités de la communauté.\n\nÀ bientôt, \n\nL’équipe Woila Community"
                # Envoi de l'email via le backend configuré dans settings.py
                send_mail(
                    sujet,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, "✅ Inscription réussie à la newsletter !")
            else:
                messages.warning(request, "⚠️ Vous êtes déjà inscrit à la newsletter.")
        # Redirige vers la page précédente pour afficher le message
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')
