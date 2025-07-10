from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.mail import send_mail

class InscriptionForm(UserCreationForm):
    """
    Formulaire d'inscription pour les nouveaux utilisateurs.
    Hérite de UserCreationForm pour inclure les champs de base.
    """
    email = forms.EmailField(required=True, help_text='Entrez une adresse e-mail valide.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': 'Le nom d’utilisateur doit être unique.',
            'email': 'Veuillez entrer une adresse e-mail valide.',
        }
        
        def save(self, commit=True):
            """
            Enregistre l'utilisateur et envoie un e-mail de confirmation.
            """
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            # Si vous souhaitez envoyer un e-mail de confirmation, vous pouvez le faire ici.
            # Par exemple, vous pouvez utiliser send_mail de django.core.mail.
            if commit:
                user.save()
                # Logique pour envoyer un e-mail de confirmation peut être ajoutée ici
            return user