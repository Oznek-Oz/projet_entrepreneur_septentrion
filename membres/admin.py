from django.contrib import admin

from membres.models import Membre, Discussion, Message


# Register your models here.

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('titre', 'auteur', 'date_creation')
    list_display_links = ('auteur', 'titre')
    search_fields = ('titre' , 'auteur' , 'date_création')
    list_filter = ('titre', 'auteur', 'date_creation')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('discussion', 'auteur', 'contenu', 'auteur_repondu', 'date_envoi')
    list_display_links = ('auteur', 'contenu', 'auteur_repondu')
    search_fields = ('auteur__username', 'contenu', 'reponse_a__auteur__username')
    list_filter = ('auteur', 'discussion')

    def auteur_repondu(self, obj):
        if obj.reponse_a and obj.reponse_a.auteur:
            return obj.reponse_a.auteur.username
        return "—"
    auteur_repondu.short_description = "Répond à"
    auteur_repondu.admin_order_field = 'reponse_a__auteur__username'
