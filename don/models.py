from django.db import models

class Don(models.Model):
    METHODE_CHOICES = [
        ("orange_money", "Orange Money"),
        ("mtn_money", "MTN Mobile Money"),
    ]
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    methode = models.CharField(max_length=20, choices=METHODE_CHOICES)
    telephone = models.CharField(max_length=20)
    date = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, default="en_attente")
    reference = models.CharField(max_length=100, blank=True, null=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} - {self.montant} FCFA ({self.methode})"

    class Meta:
        verbose_name = "Don"
        verbose_name_plural = "Dons"
