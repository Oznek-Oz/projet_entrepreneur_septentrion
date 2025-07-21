from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'sujet_short', 'statut', 'date_creation', 'actions_buttons']
    list_filter = ['statut', 'date_creation']
    search_fields = ['nom', 'email', 'sujet', 'message']
    readonly_fields = ['date_creation', 'date_lecture', 'date_reponse']
    list_per_page = 20
    
    fieldsets = (
        ('Informations du contact', {
            'fields': ('nom', 'email', 'telephone', 'sujet')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Gestion', {
            'fields': ('statut', 'reponse'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_lecture', 'date_reponse'),
            'classes': ('collapse',)
        }),
    )
    
    def sujet_short(self, obj):
        """Affiche un sujet court"""
        return obj.sujet[:50] + '...' if len(obj.sujet) > 50 else obj.sujet
    sujet_short.short_description = 'Sujet'
    
    def actions_buttons(self, obj):
        """Boutons d'action pour chaque message"""
        buttons = []
        
        if obj.statut == 'nouveau':
            buttons.append(
                f'<a href="{reverse("admin:contact_contact_change", args=[obj.id])}" '
                f'class="button" style="background: #28a745; color: white; padding: 5px 10px; '
                f'text-decoration: none; border-radius: 3px; margin-right: 5px;">Lire</a>'
            )
        
        if obj.email:
            buttons.append(
                f'<a href="mailto:{obj.email}" class="button" style="background: #007bff; '
                f'color: white; padding: 5px 10px; text-decoration: none; border-radius: 3px;">Répondre</a>'
            )
        
        return format_html(' '.join(buttons))
    actions_buttons.short_description = 'Actions'
    
    def save_model(self, request, obj, instance):
        """Marque automatiquement comme lu si l'admin modifie le statut"""
        if instance and instance.statut == 'nouveau' and obj.statut != 'nouveau':
            obj.date_lecture = timezone.now()
        super().save_model(request, obj, instance)
    
    actions = ['marquer_comme_lu', 'marquer_comme_repondu', 'archiver']
    
    def marquer_comme_lu(self, request, queryset):
        """Marque les messages sélectionnés comme lus"""
        updated = queryset.update(statut='lu', date_lecture=timezone.now())
        self.message_user(request, f'{updated} message(s) marqué(s) comme lu(s).')
    marquer_comme_lu.short_description = "Marquer comme lu"
    
    def marquer_comme_repondu(self, request, queryset):
        """Marque les messages sélectionnés comme répondus"""
        updated = queryset.update(statut='repondu', date_reponse=timezone.now())
        self.message_user(request, f'{updated} message(s) marqué(s) comme répondu(s).')
    marquer_comme_repondu.short_description = "Marquer comme répondu"
    
    def archiver(self, request, queryset):
        """Archive les messages sélectionnés"""
        updated = queryset.update(statut='archivé')
        self.message_user(request, f'{updated} message(s) archivé(s).')
    archiver.short_description = "Archiver les messages"
