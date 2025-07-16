from django.contrib import admin
from .models import Don

@admin.register(Don)
class DonAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'montant', 'methode', 'date', 'statut')
    search_fields = ('nom', 'email', 'methode')
    list_filter = ('methode', 'statut', 'date')
