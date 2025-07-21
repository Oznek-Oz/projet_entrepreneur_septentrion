import requests
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from .models import Discussion, Message, Publication
from .models import Ressource

def assistant_publication(request):
    suggestion = None
    error = None
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        if prompt:
            try:
                api_key = getattr(settings, 'OPENAI_API_KEY', None)
                if not api_key:
                    error = "Clé API OpenAI manquante."
                else:
                    response = requests.post(
                        'https://api.openai.com/v1/chat/completions',
                        headers={
                            'Authorization': f'Bearer {api_key}',
                            'Content-Type': 'application/json'
                        },
                        json={
                            'model': 'gpt-3.5-turbo',
                            'messages': [
                                {'role': 'system', 'content': 'Tu es un assistant qui aide à rédiger des publications communautaires.'},
                                {'role': 'user', 'content': prompt}
                            ],
                            'max_tokens': 300
                        }
                    )
                    if response.status_code == 200:
                        data = response.json()
                        suggestion = data['choices'][0]['message']['content']
                    else:
                        error = f"Erreur API: {response.text}"
            except Exception as e:
                error = str(e)
        # Si requête AJAX, retourne JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/x-www-form-urlencoded':
            from django.http import JsonResponse
            return JsonResponse({'suggestion': suggestion, 'error': error})
    return render(request, 'membres/assistant_publication.html', {'suggestion': suggestion, 'error': error})
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

@login_required
def messages_publication(request):
    from .models import MessagePublication
    messages_pub = MessagePublication.objects.filter(membre=request.user).order_by('-date_envoi')
    # Marquer comme lus
    messages_pub.filter(lu=False).update(lu=True)
    return render(request, 'membres/messages_publication.html', {'messages_pub': messages_pub})

# Vue pour afficher les ressources à télécharger
def ressources(request):
    ressources = Ressource.objects.all()
    return render(request, 'membres/ressources.html', {'ressources': ressources})

# Suppression multiple de publications
@login_required
@require_POST
def supprimer_publications_multiple(request):
    ids = request.POST.getlist('ids')
    pubs = Publication.objects.filter(id__in=ids)
    # On ne supprime que les publications de l'utilisateur courant ou si superuser
    for pub in pubs:
        if request.user == pub.membre or request.user.is_superuser:
            pub.delete()
    messages.success(request, "Publications supprimées avec succès !")
    return redirect('publications')
from .forms import PublicationForm
from django.urls import reverse
@login_required
def publication_modifier(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    if request.user != publication.membre and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas le droit de modifier cette publication.")
        return redirect('publications')
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES, instance=publication)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publication modifiée avec succès !')
            return redirect('publications')
    else:
        form = PublicationForm(instance=publication)
    return render(request, 'membres/publication_form.html', {'form': form, 'publication': publication})

@login_required
def publication_supprimer(request, pk):
    publication = get_object_or_404(Publication, pk=pk)
    if request.user != publication.membre and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas le droit de supprimer cette publication.")
        return redirect('publications')
    if request.method == 'POST':
        publication.delete()
        messages.success(request, 'Publication supprimée avec succès !')
        return redirect('publications')
    return render(request, 'membres/publication_confirm_delete.html', {'publication': publication})



def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': 'membres/dashboard/'})
            messages.success(request, "Connexion réussie.")
            return redirect('dashboard')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': "Nom d'utilisateur ou mot de passe invalide."})
            messages.error(request, "Nom d'utilisateur ou mot de passe invalide.")
    return render(request, 'membres/connexion.html')


@login_required(login_url = 'adhesion')
def dashboard(request):
    return render(request, 'membres/dashboard.html')




from .forms import MembreForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

@login_required
def profil(request):
    membre = request.user
    if request.method == 'POST':
        form = MembreForm(request.POST, request.FILES, instance=membre)
        if form.is_valid():
            membre = form.save()
            update_session_auth_hash(request, membre)  # Garde l'utilisateur connecté
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                from django.http import HttpResponse
                return HttpResponse('OK')
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('dashboard')  # Redirige vers le dashboard
    else:
        form = MembreForm(instance=membre)
    return render(request, 'membres/profil.html', {'form': form})


def annuaire(request):
    from .models import Membres
    membres = Membres.objects.all()
    nom = request.GET.get('nom', '').strip()
    ville = request.GET.get('ville', '').strip()
    secteur = request.GET.get('secteur', '').strip()
    statut = request.GET.get('statut', '').strip()
    if nom:
        membres = membres.filter(nom__icontains=nom)
    if ville:
        membres = membres.filter(ville__icontains=ville)
    if secteur:
        membres = membres.filter(profession__icontains=secteur)
    if statut:
        membres = membres.filter(statut__iexact=statut)
    return render(request, 'membres/annuaire.html', {
        'membres': membres,
        'search_nom': nom,
        'search_ville': ville,
        'search_secteur': secteur,
        'search_statut': statut,
    })


@login_required
def publications(request):
    publications = Publication.objects.filter(membre=request.user).order_by('-date_publication')
    form = PublicationForm()

    pub_id = request.POST.get('publication_id')
    if request.method == 'POST':
        if pub_id:
            publication = get_object_or_404(Publication, id=pub_id, membre=request.user)
            form = PublicationForm(request.POST, request.FILES, instance=publication)
            if form.is_valid():
                form.save()
                messages.success(request, 'Publication modifiée avec succès !')
                return redirect('publications')
        else:
            form = PublicationForm(request.POST, request.FILES)
            if form.is_valid():
                publication = form.save(commit=False)
                publication.membre = request.user
                publication.save()
                messages.success(request, 'Publication ajoutée avec succès !')
                return redirect('publications')

    return render(request, 'membres/publications.html', {
        'form': form,
        'publications': publications
    })

@login_required
def modifier_publication(request, id):
    publication = get_object_or_404(Publication, id=id)
    
    # Vérification des permissions
    if request.user != publication.membre and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas la permission de modifier cette publication.")
        return redirect('publications')
    
    if request.method == 'POST':
        form = PublicationForm(request.POST, request.FILES, instance=publication)
        if form.is_valid():
            form.save()
            messages.success(request, 'Publication modifiée avec succès !')
            return redirect('publications')
    else:
        form = PublicationForm(instance=publication)
    
    return render(request, 'membres/modifier_publication.html', {
        'form': form,
        'publication': publication
    })

@login_required
def supprimer_publication(request, id):
    publication = get_object_or_404(Publication, id=id)
    # Vérification des permissions
    if request.user != getattr(publication.membre, 'user', publication.membre) and not request.user.is_superuser:
        messages.error(request, "Vous n'avez pas la permission de supprimer cette publication.")
        return redirect('publications')

    if request.method == 'POST':
        membre = getattr(publication.membre, 'user', publication.membre)
        titre = publication.titre
        publication.delete()
        # Si c'est un admin, possibilité d'envoyer un message au membre
        if request.user.is_superuser:
            from .models import MessagePublication
            MessagePublication.objects.create(
                membre=membre,
                publication_titre=titre,
                message="Votre publication a été supprimée car elle ne respecte pas les standards de la communauté.",
            )
        messages.success(request, 'Publication supprimée avec succès !')
        return redirect('publications')

    return render(request, 'membres/supprimer_publication.html', {
        'publication': publication
    })

@login_required
def forum(request):
    return redirect('forum_list')
    #return render(request, 'membres/forum_list.html')


# Liste des discussions
@login_required
def forum_list(request):
    discussions = Discussion.objects.order_by('-date_creation')
    return render(request, 'membres/forum_list.html', {'discussions': discussions})


# Détail d'une discussion
@login_required
def forum_detail(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    messages_list = discussion.messages.order_by('id')
    return render(request, 'membres/forum_detail.html', {'discussion': discussion, 'messages': messages_list})


# Création d'une discussion
@login_required
def forum_create(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.POST.get('contenu')
        if titre and contenu:
            discussion = Discussion.objects.create(titre=titre, auteur=request.user)
            Message.objects.create(discussion=discussion, auteur=request.user, contenu=contenu)
            return redirect('forum_detail', pk=discussion.pk)
        messages.error(request, 'Veuillez remplir tous les champs.')
    return render(request, 'membres/forum_form.html')


# Répondre à une discussion
@login_required
def forum_reply(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        reponse_a_id = request.POST.get('reponse_a')
        reponse_a = None
        if reponse_a_id:
            try:
                reponse_a = Message.objects.get(id=reponse_a_id)
            except Message.DoesNotExist:
                reponse_a = None
        if contenu:
            Message.objects.create(
                discussion=discussion,
                auteur=request.user,
                contenu=contenu,
                reponse_a=reponse_a
            )
            return redirect('forum_detail', pk=discussion.pk)
        messages.error(request, 'Le message ne peut pas être vide.')
    return redirect('forum_detail', pk=discussion.pk)


# Suppression d'une discussion (admin seulement)
@user_passes_test(lambda u: u.is_staff)
def forum_delete(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if request.user == discussion.auteur or request.user.is_superuser:
        discussion.delete()
        return redirect('forum')
    messages.error(request, "Vous n'avez pas le droit de supprimer cette discussion.")
    return redirect('forum_detail', pk=discussion.pk)


@login_required
# Déconnexion d'un utilisateur
def deconnexion(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('accueil')
