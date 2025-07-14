from django.shortcuts import render

def galerie(request):
    """
    Render the gallery page.
    """
    return render(request, 'galerie/galery.html')