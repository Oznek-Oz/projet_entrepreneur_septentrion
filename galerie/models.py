from django.db import models

# Create your models here.
class Galerie(models.Model):
    TYPE_CHOICES = [
        ('photo', 'Photo'),
        ('video', 'Vidéo'),
    ]

    titre = models.CharField(max_length=255)
    type_media = models.CharField(max_length=10, choices=TYPE_CHOICES)
    chemin_fichier = models.CharField(max_length=255)
    evenement = models.CharField(max_length=255)
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
