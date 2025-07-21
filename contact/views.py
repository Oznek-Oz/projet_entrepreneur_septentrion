from os import name
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Contact

# Create your views here.

def contact(request):
    """Vue pour gérer le formulaire de contact"""
    if request.method == 'POST':
        # Récupération des données du formulaire
        nom = request.POST.get('nom', '').strip()
        email = request.POST.get('email', '').strip()
        sujet = request.POST.get('sujet', '').strip()
        message = request.POST.get('message', '').strip()
        telephone = request.POST.get('telephone', '').strip()
        
        # Validation des champs requis
        if not nom or not email or not message:
            messages.error(request, "Veuillez remplir tous les champs obligatoires.")
            return render(request, 'contact/contact.html', {
                'nom': nom,
                'email': email,
                'sujet': sujet,
                'message': message,
                'telephone': telephone
            })
        
        # Validation de l'email
        if '@' not in email or '.' not in email:
            messages.error(request, "Veuillez entrer une adresse email valide.")
            return render(request, 'contact/contact.html', {
                'nom': nom,
                'email': email,
                'sujet': sujet,
                'message': message,
                'telephone': telephone
            })
        
        try:
            # Création du message de contact
            contact = Contact.objects.create(
                nom=nom,
                email=email,
                sujet=sujet,
                message=message,
                telephone=telephone
            )
            
            # Notification par email aux administrateurs
            notify_admins(contact)
            
            messages.success(request, "Votre message a été envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.")
            return redirect('contact:contact')
            
        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de l'envoi du message. Veuillez réessayer. ({str(e)})")
            return render(request, 'contact/contact.html', {
                'nom': nom,
                'email': email,
                'sujet': sujet,
                'message': message,
                'telephone': telephone
            })
    
    return render(request, 'contact/contact.html')

def notify_admins(contact):
    """Envoie une notification par email aux administrateurs"""
    try:
        # Récupération des administrateurs
        admins = User.objects.filter(is_staff=True, is_active=True)
        
        if not admins.exists():
            return
        
        # Préparation du message
        subject = f"Nouveau message de contact - {contact.nom}"
        message = f"""
Nouveau message de contact reçu :

Nom : {contact.nom}
Email : {contact.email}
Téléphone : {contact.telephone or 'Non renseigné'}
Sujet : {contact.sujet or 'Aucun sujet'}

Message :
{contact.message}

Date : {contact.date_creation.strftime('%d/%m/%Y à %H:%M')}

Pour répondre, connectez-vous à l'interface d'administration.
        """
        
        # Envoi aux administrateurs
        admin_emails = [admin.email for admin in admins if admin.email]
        
        if admin_emails:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=admin_emails,
                fail_silently=True
            )
    
    except Exception as e:
        # En cas d'erreur, on ne bloque pas le processus
        print(f"Erreur lors de l'envoi de notification: {e}")
        pass
