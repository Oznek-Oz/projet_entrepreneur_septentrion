"""from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.mail import send_mail

class InscriptionForm(UserCreationForm):
    
    #Formulaire d'inscription pour les nouveaux utilisateurs.
    #Hérite de UserCreationForm pour inclure les champs de base.
    
    email = forms.EmailField(required=True, help_text='Entrez une adresse e-mail valide.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': 'Le nom d’utilisateur doit être unique.',
            'email': 'Veuillez entrer une adresse e-mail valide.',
        }
        
        def save(self, commit=True):
            
            #Enregistre l'utilisateur et envoie un e-mail de confirmation.
            
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']
            # Si vous souhaitez envoyer un e-mail de confirmation, vous pouvez le faire ici.
            # Par exemple, vous pouvez utiliser send_mail de django.core.mail.
            if commit:
                user.save()
                # Logique pour envoyer un e-mail de confirmation peut être ajoutée ici
            return user"""
"""from django import forms
from .models import Membre
from django.contrib.auth.hashers import make_password

class MembreForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirmer le mot de passe")
    password = forms.CharField(widget=forms.PasswordInput(), label="Mot de passe")

    class Meta:
        model = Membre
        # Liste les champs que tu veux dans le formulaire (pas forcément tous)
        fields = [
            'username', 'nom', 'prenom', 'email', 'password', 'confirm_password', 'photo',
            'ville', 'profession', 'statut', 'mini_cv',
            'facebook', 'linkedin', 'twitter',
            'type_adhesion', 'date_adhesion', 'montant',
            'moyen_paiement', 'numero_transaction',
        ]

        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'ville': forms.TextInput(attrs={'class': 'form-control'}),
            'profession': forms.TextInput(attrs={'class': 'form-control'}),
            'statut': forms.TextInput(attrs={'class': 'form-control'}),
            'mini_cv': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'type_adhesion': forms.Select(attrs={'class': 'form-select'}),
            'date_adhesion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'max': '99999999.99'}),
            'moyen_paiement': forms.Select(attrs={'class': 'form-select'}),
            'numero_transaction': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Les mots de passe ne correspondent pas.")

        return cleaned_data

    def save(self, commit=True):
        membre = super().save(commit=False)
        # Hasher le mot de passe avant sauvegarde
        membre.password = make_password(self.cleaned_data["password"])
        if commit:
            membre.save()
        return membre
"""
