"""
Modèle pour les abonnés à la newsletter.
Chaque instance représente un email inscrit à la newsletter.
"""

from django.db import models

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)  # Adresse email de l'abonné (unique)
    date_inscription = models.DateTimeField(auto_now_add=True)  # Date d'inscription automatique

    def __str__(self):
        """
        Retourne l'email pour l'affichage dans l'admin Django.
        """
        return self.email
