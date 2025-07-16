from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Discussion, Message
from django.urls import reverse


def connexion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        #if user is not None and user.is_actif:
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


@login_required
def dashboard(request):
    return render(request, 'membres/dashboard.html')

@login_required
def profil(request):
    return render(request, 'membres/profil.html')


def annuaire(request):
    return render(request, 'membres/annuaire.html')

@login_required
def publications(request):
    return render(request, 'membres/publications.html')

@login_required
def ressources(request):
    return render(request, 'membres/ressources.html')

@login_required
def forum(request):
    return render(request, 'membres/forum.html')


# Liste des discussions
@login_required
def forum_list(request):
    discussions = Discussion.objects.order_by('-date_creation')
    return render(request, 'membres/forum_list.html', {'discussions': discussions})


# Détail d'une discussion
@login_required
def forum_detail(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    messages = discussion.messages.order_by('date_envoi')
    return render(request, 'membres/forum_detail.html', {'discussion': discussion, 'messages': messages})


# Création d'une discussion
@login_required
def forum_create(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        contenu = request.POST.get('contenu')
        if titre and contenu:
            discussion = Discussion.objects.create(titre=titre, auteur=request.user)
            Message.objects.create(discussion=discussion, auteur=request.user, contenu=contenu)
            return redirect(reverse('forum_detail', args=[discussion.id]))
    return render(request, 'membres/forum_form.html')


# Répondre à une discussion
@login_required
def forum_reply(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    if request.method == 'POST':
        contenu = request.POST.get('contenu')
        reponse_a_id = request.POST.get('reponse_a')
        reponse_a = Message.objects.filter(id=reponse_a_id).first() if reponse_a_id else None
        if contenu:
            Message.objects.create(discussion=discussion, auteur=request.user, contenu=contenu, reponse_a=reponse_a)
    return redirect(reverse('forum_detail', args=[discussion.id]))


# Suppression d'une discussion (admin seulement)
@user_passes_test(lambda u: u.is_staff)
def forum_delete(request, pk):
    discussion = get_object_or_404(Discussion, pk=pk)
    discussion.delete()
    return redirect('forum_list')
