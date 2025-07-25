from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, User
from django.db import models
from django.utils import timezone
from django.conf import settings

# Ressources à télécharger (mémoire, CV, cours, etc.)
class Ressource(models.Model):
    CATEGORIES = [
        ("memoire", "Mémoire"),
        ("cv", "Modèle de CV"),
        ("cours", "Cours"),
        ("guide", "Guide"),
        ("autre", "Autre"),
    ]
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fichier = models.FileField(upload_to="ressources/")
    categorie = models.CharField(max_length=20, choices=CATEGORIES, default="autre")
    date_ajout = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
"""
Modèles pour la gestion des membres de la communauté.
Inclut un utilisateur personnalisé (Membre) avec de nombreux champs de profil.
"""


class MembreManager(BaseUserManager):
    """
    Manager personnalisé pour le modèle Membre.
    Permet de créer des utilisateurs et des superutilisateurs avec des champs personnalisés.
    """
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Le nom d'utilisateur est obligatoire")
        if not email:
            raise ValueError("L'email est obligatoire")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class Membres(AbstractBaseUser, PermissionsMixin):
    """
    Modèle principal représentant un membre de la communauté.
    Hérite de AbstractBaseUser pour la personnalisation complète de l'utilisateur.
    """
    username = models.CharField(max_length=100, unique=True)  # Identifiant unique
    nom = models.CharField(max_length=100)  # Nom de famille
    prenom = models.CharField(max_length=100)  # Prénom
    email = models.EmailField(unique=True)  # Email unique
    password = models.CharField(max_length=100)  # Mot de passe (haché)
    photo = models.ImageField(upload_to='membres/photos/', null=True, blank=True)  # Photo de profil
    ville = models.CharField(max_length=100, blank=True)  # Ville de résidence
    profession = models.CharField(max_length=100, blank=True)  # Profession
    statut = models.CharField(max_length=50, blank=True)  # Statut (étudiant, pro, etc.)
    mini_cv = models.TextField(null=True, blank=True)  # Mini CV
    facebook = models.URLField(null=True, blank=True)  # Lien Facebook
    linkedin = models.URLField(null=True, blank=True)  # Lien LinkedIn
    twitter = models.URLField(null=True, blank=True)  # Lien Twitter

    numero_adherent = models.CharField(max_length=20, unique=True, editable=False, blank=True)  # Numéro d'adhérent généré automatiquement

    TYPE_CHOICES = [
        ('etudiant', 'Étudiant'),
        ('freelance', 'Freelance'),
        ('entrepreneur', 'Entrepreneur'),
        ('autre', 'Autre'),
    ]
    type_adhesion = models.CharField(max_length=20, choices=TYPE_CHOICES, null=True, blank=True)  # Type d'adhésion
    confirmation_token = models.CharField(max_length=100, null=True, blank=True, unique=True)
    is_confirmed = models.BooleanField(default=False)
    date_adhesion = models.DateField(null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    moyen_paiement = models.CharField(max_length=50, null=True, blank=True)
    numero_transaction = models.CharField(max_length=100, null=True, blank=True)

    date_inscription = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)  # Champ requis pour AbstractBaseUser
    is_staff = models.BooleanField(default=False)  # accès admin

    is_promoteur = models.BooleanField(default=False, help_text="Ce membre est un promoteur de l'association.")
    objects = MembreManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nom', 'prenom']

    def save(self, *args, **kwargs):
        if not self.numero_adherent:
            dernier_id = Membres.objects.count() + 1
            self.numero_adherent = f"ADH{dernier_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.prenom} {self.nom}"

class Discussion(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre

class MessagePublication(models.Model):
    from django.conf import settings
    membre = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_publication')
    publication_titre = models.CharField(max_length=255)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)

    def __str__(self):
        return f"Message à {self.membre.username} concernant '{self.publication_titre}'"
class Message(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='messages')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    reponse_a = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.auteur.username}: {self.contenu[:30]}..."


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
    fichier_joint = models.FileField(upload_to='publications/', blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    valide = models.BooleanField(default=False, help_text="La publication doit être validée par un administrateur pour être affichée.")

    def __str__(self):
        return self.titre