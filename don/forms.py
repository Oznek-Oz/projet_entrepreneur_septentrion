from django import forms
from .models import Don

class DonForm(forms.ModelForm):
    class Meta:
        model = Don
        fields = ['nom', 'email', 'montant']
        widgets = {
            'montant': forms.NumberInput(attrs={'min': 1000, 'step': 100, 'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        
    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if telephone:
            # Nettoyer le numéro de téléphone
            telephone = ''.join(filter(str.isdigit, telephone))
            if len(telephone) != 10:
                raise forms.ValidationError("Le numéro de téléphone doit contenir 10 chiffres.")
        return telephone
    
    def clean_montant(self):
        montant = self.cleaned_data.get('montant')
        if montant and montant < 100:
            raise forms.ValidationError("Le montant minimum est de 100 FCFA.")
        return montant 