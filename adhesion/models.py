from django.db import models
from membres.models import Membres

# Create your models here.

class Adhesion (models.Model):
    TYPE_CHOICES = [
        ('etudiant', 'Etudiant'),
        ('freelance', 'Freelance'),
        ('entrepreneur', 'Entrepreneur'),
        ('autres', 'Autres')
    ]
    
    numero_adherent = models.CharField(max_length=20)
    membre = models.ForeignKey(Membres, on_delete = models.CASCADE)
    type_adhesion = models.CharField(max_length=20, choices=TYPE_CHOICES)
    montant = models.DecimalField(max_digits=10, decimal_places=5)
    moyen_paiment = models.CharField(max_length=50)
    numero_transaction = models.CharField(max_length=100)
    def __str__(self):
        return self.numero_adherent
