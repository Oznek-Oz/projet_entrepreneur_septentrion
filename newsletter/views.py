from django.contrib import messages
from django.shortcuts import redirect
from .models import NewsletterSubscriber

def inscription_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                NewsletterSubscriber.objects.create(email=email)
                messages.success(request, "✅ Inscription réussie à la newsletter !")
            else:
                messages.warning(request, "⚠️ Vous êtes déjà inscrit à la newsletter.")
        # On revient à la même page pour afficher le popup via messages
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')
