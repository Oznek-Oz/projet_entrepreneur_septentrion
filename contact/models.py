from django.db import models
from django.utils import timezone

class Contact(models.Model):
    STATUT_CHOICES = [
        ('nouveau', 'Nouveau'),
        ('lu', 'Lu'),
        ('repondu', 'Répondu'),
        ('archivé', 'Archivé'),
    ]
    
    nom = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Adresse email")
    sujet = models.CharField(max_length=200, verbose_name="Sujet", blank=True)
    message = models.TextField(verbose_name="Message")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone", blank=True)
    date_creation = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='nouveau', verbose_name="Statut")
    date_lecture = models.DateTimeField(null=True, blank=True, verbose_name="Date de lecture")
    reponse = models.TextField(blank=True, verbose_name="Réponse administrateur")
    date_reponse = models.DateTimeField(null=True, blank=True, verbose_name="Date de réponse")
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"{self.nom} - {self.sujet or 'Sans sujet'} ({self.date_creation.strftime('%d/%m/%Y')})"
    
    def marquer_comme_lu(self):
        """Marque le message comme lu"""
        from django.utils import timezone
        self.statut = 'lu'
        self.date_lecture = timezone.now()
        self.save()
    
    def repondre(self, reponse_text):
        """Ajoute une réponse au message"""
        from django.utils import timezone
        self.statut = 'repondu'
        self.reponse = reponse_text
        self.date_reponse = timezone.now()
        self.save()
