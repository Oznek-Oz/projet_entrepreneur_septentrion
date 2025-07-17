from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

# galerie/views.py
from .models import Image
from .models import Image


def galerie(request):
    carousel_images = Image.objects.filter(afficher_dans_carousel=True).order_by('-date_ajout')[:3]
    return render(request, 'galerie.html', {'carousel_images': carousel_images})


def galerie_view(request):
    images = Image.objects.order_by('-date_ajout')
    return render(request, 'galerie/galerie.html', {'images': images})


def galerie_filtre(request, origine):
    images = Image.objects.filter(origine=origine).order_by('-date_ajout')

    # Détection de l'origine
    """if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('galerie/_cards.html', {'images': images}, request=request)
        return JsonResponse({'html': html})"""

    return render(request, 'galerie/galerie.html', {'images': images, 'filtre': origine})


def upload_multiple_images(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        origine = request.POST.get('origine')
        type_media = request.POST.get('type_media')
        description = request.POST.get('description')
        date_ajout = request.POST.get('date_ajout')

        images = request.FILES.getlist('images')  # liste des fichiers uploadés

        for image_file in images:
            Image.objects.create(
                titre=titre,
                origine=origine,
                type_media=type_media,
                description=description,
                image=image_file,
            )
        return redirect('galerie')  # ou autre page

    return render(request, 'galerie/galerie.html')
