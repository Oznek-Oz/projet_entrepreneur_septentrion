from django import forms
from .models import Don

class DonForm(forms.ModelForm):
    class Meta:
        model = Don
        fields = [
            'nom', 'email', 'montant', 'methode',
            'telephone', 'nom_carte', 'numero_carte', 'expiration', 'cvv'
        ]
        widgets = {
            'methode': forms.Select(attrs={'class': 'form-select', 'id': 'id_methode'}),
            'montant': forms.NumberInput(attrs={'min': 1000, 'step': 100, 'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de téléphone Mobile Money'}),
            'nom_carte': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom sur la carte'}),
            'numero_carte': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Numéro de carte'}),
            'expiration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/AA'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV'}),
        }
