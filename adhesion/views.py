from django.shortcuts import render

# Create your views here.
def adhesion(request):
    """
    Render the home page.
    """
    return render(request, 'adhesion/adhesion.html')