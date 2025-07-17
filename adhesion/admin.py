from django.contrib import admin

from membres.models import Membres

# Register your models here.

@admin.register(Membres)
class Membres(admin.ModelAdmin):
    list_display = ('numero_adherent', 'username' , 'prenom', 'nom', 'email', 'ville', 'statut' , 'montant' , 'date_adhesion')
    readonly_fields = ('numero_adherent',)
