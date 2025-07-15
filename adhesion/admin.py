from django.contrib import admin

from membres.models import Membre

# Register your models here.

@admin.register(Membre)
class Membre(admin.ModelAdmin):
    list_display = ('numero_adherent', 'username' , 'prenom', 'nom', 'email', 'ville', 'statut' , 'montant' , 'date_adhesion')
    readonly_fields = ('numero_adherent',)
