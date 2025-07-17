from django.db import models

# galerie/models.py
from django.db import models


class Image(models.Model):
    TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Vidéo'),
    ]
    ORIGINE_CHOICES = [
        ('profil', 'Photo de profil'),
        ('userpost', 'Post utilisateur'),
        ('blog', 'Blog'),
        ('galerie', 'Galerie'),
    ]
    type_media = models.CharField(max_length=10, choices=TYPE_CHOICES)

    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='galerie/')
    origine = models.CharField(max_length=20, choices=ORIGINE_CHOICES)
    date_ajout = models.DateTimeField(auto_now_add=True)

    afficher_dans_carousel = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titre} ({self.get_origine_display()})"
