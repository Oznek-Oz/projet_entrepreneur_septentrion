from django.db import models

# Create your models here.

class Administrateur(models.Model):
    nom_utilisateur = models.CharField(max_length=100, unique=True)
    mot_de_passe = models.CharField(max_length=255)

    def __str__(self):
        return self.nom_utilisateur
