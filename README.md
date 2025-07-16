# Woila Community

Projet Django pour la gestion d'une communauté avec newsletter, adhésion, blog, galerie, forum, etc.

## Installation

1. **Cloner le projet**
   ```bash
   git clone <url-du-repo>
   cd woila_community
   ```
2. **Créer et activer un environnement virtuel**
   ```bash
   python -m venv env
   env\Scripts\activate  # Windows
   source env/bin/activate  # Linux/Mac
   ```
3. **Installer les dépendances**
   ```bash
   pip install django
   # Ajouter ici les autres dépendances si besoin
   ```
4. **Configurer la base de données**
   ```bash
   python manage.py migrate
   ```
5. **Créer un superutilisateur**
   ```bash
   python manage.py createsuperuser
   ```
6. **Lancer le serveur**
   ```bash
   python manage.py runserver
   ```

## Configuration de l'envoi d'emails

Dans `monsite/settings.py` :
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'votre_email@gmail.com'
EMAIL_HOST_PASSWORD = 'votre_mot_de_passe'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

## Fonctionnalités principales

- **Newsletter** : Inscription et envoi d'emails de remerciement personnalisés.
- **Adhésion** : Inscription, envoi d'email de confirmation avec lien unique, validation d'adhésion.
- **Blog** : Gestion des articles et commentaires.
- **Galerie** : Ajout et affichage d'images.
- **Forum** : Discussions et messages entre membres.

## Structure du projet

- `accueil/` : Page d'accueil et vues principales
- `adhesion/` : Gestion des adhésions
- `admin/` : Administration personnalisée
- `blog/` : Articles et commentaires
- `contact/` : Formulaire de contact
- `galerie/` : Galerie d'images
- `membres/` : Modèle utilisateur personnalisé
- `newsletter/` : Gestion de la newsletter
- `polls/` : Sondages
- `projets/` : Projets de la communauté
- `static/` : Fichiers statiques (CSS, JS, images)
- `templates/` : Templates HTML
- `monsite/` : Configuration principale du projet

## Exemples de code

### Envoi d'un email de remerciement (newsletter/views.py)
```python
# ...
from django.core.mail import send_mail
# ...
def inscription_newsletter(request):
    # ...
    send_mail(
        sujet,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=False,
    )
    # ...
```

### Envoi d'un email de confirmation avec lien (adhesion/views.py)
```python
# ...
confirmation_url = request.build_absolute_uri(
    reverse('adhesion:confirmer', args=[membre.confirmation_token])
)
send_mail(
    sujet,
    message,
    settings.DEFAULT_FROM_EMAIL,
    [membre.email],
    fail_silently=False,
)
# ...
```

## Commentaires et documentation dans le code

- Chaque vue, modèle et fonction importante est commentée pour expliquer son rôle.
- Les docstrings sont ajoutés dans les fichiers Python pour faciliter la compréhension.

## Auteur

Projet réalisé par Tchikaya Famikenzo Franck

---
Pour toute question, consultez la documentation Django officielle : https://docs.djangoproject.com/fr/

