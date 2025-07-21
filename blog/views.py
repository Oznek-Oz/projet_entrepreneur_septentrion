from django.shortcuts import render

# Create your views here.
from membres.models import Publication
def blog(request):
    publications = Publication.objects.filter(valide=True).order_by('-date_publication')
    recent_publications = publications[:5]
    return render(request, 'blog/blog.html', {
        'publications': publications,
        'recent_publications': recent_publications
    })

