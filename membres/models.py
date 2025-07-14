from django.db import models

# Create your models here.

class Membres(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=100)
    photo = models.CharField(max_length=100)
    ville = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)
    statut = models.CharField(max_length=50)
    mini_cv = models.TextField()
    date_inscription = models.DateTimeField(auto_now_add=True)
    is_actif = models.BooleanField(default=True)   
    def __str__(self):
        return f"{self.prenom} {self.nom}"
