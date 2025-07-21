from django.contrib import admin
from .models import Publication, Ressource, MessagePublication, Membres
@admin.register(Membres)
class MembresAdmin(admin.ModelAdmin):
    list_display = ('prenom', 'nom', 'email', 'profession', 'is_promoteur', 'is_actif')
    list_filter = ('is_promoteur', 'is_actif', 'profession')
    search_fields = ('prenom', 'nom', 'email', 'profession')

class PublicationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'membre', 'type', 'date_publication', 'valide')
    list_filter = ('type', 'valide', 'date_publication')
    search_fields = ('titre', 'description', 'membre__username')
    actions = ['valider_publications']

    def valider_publications(self, request, queryset):
        queryset.update(valide=True)
        self.message_user(request, "Les publications sélectionnées ont été validées.")
    valider_publications.short_description = "Valider les publications sélectionnées"

admin.site.register(Publication, PublicationAdmin)
admin.site.register(Ressource)

@admin.register(MessagePublication)
class MessagePublicationAdmin(admin.ModelAdmin):
    list_display = ('membre', 'publication_titre', 'date_envoi', 'lu')
    list_filter = ('lu', 'date_envoi')
    search_fields = ('membre__username', 'publication_titre', 'message')
