from django.db import models
from membres.models import Membres

class Publication(models.Model):
    TYPE_CHOICES = [
        ('projet', 'Projet'),
        ('offre', 'Offre'),
        ('evenement', 'Événement'),
    ]

    membre = models.ForeignKey(Membres, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    fichier_joint = models.CharField(max_length=255, blank=True)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
