from django.db import models

class Don(models.Model):
    METHODE_CHOICES = [
        ("orange_money", "Orange Money"),
        ("mtn_money", "MTN Mobile Money"),
        ("carte", "Carte bancaire"),
    ]
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    methode = models.CharField(max_length=20, choices=METHODE_CHOICES)
    date = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, default="en_attente")
    reference = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    # Champs pour carte bancaire
    nom_carte = models.CharField(max_length=100, blank=True, null=True)
    numero_carte = models.CharField(max_length=20, blank=True, null=True)
    expiration = models.CharField(max_length=7, blank=True, null=True)  # MM/AA
    cvv = models.CharField(max_length=4, blank=True, null=True)

    def __str__(self):
        return f"{self.nom} - {self.montant} FCFA ({self.methode})"
