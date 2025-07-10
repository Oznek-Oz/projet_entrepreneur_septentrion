from django.shortcuts import redirect, render
from .forms import InscriptionForm
from django.contrib.auth import login, authenticate
# Create your views here.

def inscription(request):
    """
    View to handle user registration.
    """
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically log in the user after registration
            login(request, user)
            return render(request, '/', {'user': user})
    else:
        form = InscriptionForm()
        return render(request, 'membres/inscription.html', {'form': form})
    return HttpResponse("Test: vue inscription OK")