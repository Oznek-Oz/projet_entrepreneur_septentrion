from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect

from .models import NewsletterSubscriber
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@csrf_exempt
def inscription_newsletter(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        email = request.POST.get('email')
        if not email:
            return JsonResponse({'success': False, 'message': "Veuillez fournir une adresse e-mail."})
        if NewsletterSubscriber.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': "Cet e-mail est déjà inscrit à la newsletter."})
        NewsletterSubscriber.objects.create(email=email)
        return JsonResponse({'success': True,
                             'message': "Merci pour votre inscription à la newsletter. Vous serez informé des nouveautés."})
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if not NewsletterSubscriber.objects.filter(email=email).exists():
                NewsletterSubscriber.objects.create(email=email)
                sujet = "Merci pour votre inscription à la newsletter !"
                message = f"Bonjour,\n\nMerci de vous être inscrit à notre newsletter. Vous serez informé des nouveautés et actualités de la communauté.\n\nÀ bientôt, \n\nL’équipe Woila Community"
                send_mail(
                    sujet,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, "✅ Inscription réussie à la newsletter !")
            else:
                messages.warning(request, "⚠️ Vous êtes déjà inscrit à la newsletter.")
        return redirect(request.META.get('HTTP_REFERER', '/'))
    return redirect('/')
