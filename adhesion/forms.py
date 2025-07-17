from django import forms
from membres.models import Membres
from decimal import Decimal

class MembreForm(forms.ModelForm):
    class Meta:
        model = Membres
        exclude = ['numero_adherent', 'date_inscription', 'is_actif']

    def clean_montant(self):
        montant = self.cleaned_data.get('montant')
        if montant and montant > Decimal("99999999.99"):
            raise forms.ValidationError("Le montant ne peut pas dépasser 99 999 999.99 FCFA.")
        return montant
