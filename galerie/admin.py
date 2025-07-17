from django.contrib import admin
from .models import Image
from django.utils.html import format_html


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('titre', 'origine', 'type_media', 'date_ajout', 'image_preview' , 'afficher_dans_carousel')
    list_filter = ('origine', 'type_media', 'date_ajout' , 'titre' , 'afficher_dans_carousel')
    list_editable = ('afficher_dans_carousel',)
    search_fields = ('titre', 'description')
    readonly_fields = ('image_preview',)
    fieldsets = (
        (None, {
            'fields': ('titre', 'description', 'origine', 'type_media', 'image', 'image_preview')
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="auto" />', obj.image.url)
        return "(Aucune image)"
    image_preview.short_description = "Aperçu"
