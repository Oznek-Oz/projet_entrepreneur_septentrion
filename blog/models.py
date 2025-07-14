from django.db import models
from membres.models import Membres

class Actualite(models.Model):
    auteur = models.ForeignKey(Membres, on_delete=models.SET_NULL, null=True)
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    image = models.CharField(max_length=255, blank=True)
    fichier_joint = models.CharField(max_length=255, blank=True)
    categorie = models.CharField(max_length=100)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
