import requests
import uuid
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from .models import Don
from .forms import DonForm
from django.urls import reverse

def don(request):
    """
    Vue pour gérer le formulaire de don et initier le paiement CinetPay.
    """
    if request.method == 'POST':
        form = DonForm(request.POST)
        if form.is_valid():
            don = form.save(commit=False)
            don.methode = 'mobile_money'  # CinetPay gère automatiquement tous les opérateurs
            don.statut = 'en_attente'
            don.save()
            
            try:
                return redirect('don:cinetpay_init', don_id=don.id)
            except Exception as e:
                don.statut = 'échoué'
                don.message = f"Erreur lors de l'initialisation: {str(e)}"
                don.save()
                messages.error(request, "Erreur lors de l'initialisation du paiement. Veuillez réessayer.")
                return render(request, 'don/don_form.html', {'form': form})
    else:
        form = DonForm()
    
    return render(request, 'don/don_form.html', {'form': form})


def cinetpay_init(request, don_id):
    """
    Initialise le paiement CinetPay pour un don.
    """
    don = get_object_or_404(Don, id=don_id)
    
    # Configuration CinetPay
    api_key = getattr(settings, 'CINETPAY_API_KEY', '')
    site_id = getattr(settings, 'CINETPAY_SITE_ID', '')
    
    if not api_key or not site_id:
        don.statut = 'échoué'
        don.message = "Configuration CinetPay manquante"
        don.save()
        messages.error(request, "Configuration de paiement manquante. Contactez l'administrateur.")
        return redirect('don:don')
    
    # URLs de callback
    base_url = getattr(settings, 'BASE_URL', 'http://localhost:8000')
    notify_url = f"{base_url}/don/cinetpay/notify/"
    return_url = f"{base_url}/don/cinetpay/return/"
    
    # Génération de l'ID de transaction
    transaction_id = f"DON_{don.id}_{str(uuid.uuid4())[:8]}"
    don.transaction_id = transaction_id
    don.reference = transaction_id
    don.save()
    
    # Préparation des données pour CinetPay
    data = {
        'apikey': api_key,
        'site_id': site_id,
        'transaction_id': transaction_id,
        'amount': int(float(don.montant)),
        'currency': 'XAF',  # Changé de XOF à XAF pour correspondre à ton compte CinetPay
        'description': f"Don de {don.nom} - {don.montant} FCFA",
        'notify_url': notify_url,
        'return_url': return_url,
        'channels': 'MOBILE_MONEY',  # CinetPay accepte : ALL, MOBILE_MONEY, WALLET, CREDIT_CARD, INTERNATIONAL_CARD
        'customer_name': don.nom,
        'customer_surname': don.nom,
        'customer_email': don.email,
        'customer_address': '',
        'customer_city': '',
        'customer_country': 'CM',
        'customer_zip_code': '',
        'customer_state': '',
    }
    
    try:
        url = 'https://api-checkout.cinetpay.com/v2/payment'
        #url = 'https://sandbox.cinetpay.com/api/v1/payment'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers, timeout=30)
        result = response.json()
        
        print(f"DEBUG - CinetPay Response: {result}")  # Debug
        
        if result.get('code') == '201' or result.get('code') == '200':
            payment_url = result['data']['payment_url']
            return redirect(payment_url)
        else:
            error_msg = result.get('description', 'Erreur CinetPay inconnue')
            print(f"DEBUG - CinetPay Error: {error_msg}")  # Debug
            don.statut = 'échoué'
            don.message = f"Erreur CinetPay: {error_msg}"
            don.save()
            messages.error(request, f"Erreur de paiement: {error_msg}")
            return redirect('don:don')
            
    except requests.exceptions.RequestException as e:
        print(f"DEBUG - Network Error: {str(e)}")  # Debug
        don.statut = 'échoué'
        don.message = f"Erreur réseau: {str(e)}"
        don.save()
        messages.error(request, "Erreur de connexion au service de paiement. Veuillez réessayer.")
        return redirect('don:don')


def cinetpay_return(request):
    """
    Gère le retour de l'utilisateur après paiement CinetPay.
    """
    transaction_id = request.GET.get('transaction_id')
    status = request.GET.get('status', '')
    
    if not transaction_id:
        messages.error(request, "Transaction inconnue.")
        return redirect('don:don')
    
    try:
        don = get_object_or_404(Don, transaction_id=transaction_id)
        
        if status == 'SUCCESS':
            don.statut = 'payé'
            don.save()
            return render(request, 'don/don_success.html', {'don': don})
        elif status == 'FAILED':
            don.statut = 'échoué'
            don.message = "Paiement échoué"
            don.save()
            messages.error(request, "Le paiement a échoué. Veuillez réessayer.")
            return redirect('don:don')
        else:
            # Statut en attente ou autre
            return render(request, 'don/don_pending.html', {'don': don})
            
    except Exception:
        messages.error(request, "Transaction introuvable.")
        return redirect('don:don')


@csrf_exempt
def cinetpay_notify(request):
    """
    Notification serveur à serveur de CinetPay.
    """
    if request.method != 'POST':
        return HttpResponse(status=405)
    
    try:
        data = json.loads(request.body)
        transaction_id = data.get('transaction_id')
        status = data.get('status')
        
        if not transaction_id:
            return HttpResponse(status=400)
        
        try:
            don = get_object_or_404(Don, transaction_id=transaction_id)
            
            if status == 'ACCEPTED':
                don.statut = 'payé'
                don.message = "Paiement confirmé par CinetPay"
            elif status == 'REFUSED':
                don.statut = 'échoué'
                don.message = "Paiement refusé par CinetPay"
            elif status == 'PENDING':
                don.statut = 'en_attente'
                don.message = "Paiement en attente de confirmation"
            else:
                don.statut = 'échoué'
                don.message = f"Statut inconnu: {status}"
            
            don.save()
            return HttpResponse(status=200)
            
        except Exception:
            return HttpResponse(status=404)
            
    except json.JSONDecodeError:
        return HttpResponse(status=400)
    except Exception as e:
        return HttpResponse(status=500)


def don_status(request, don_id):
    """
    API pour vérifier le statut d'un don.
    """
    try:
        don = get_object_or_404(Don, id=don_id)
        return JsonResponse({
            'id': don.id,
            'statut': don.statut,
            'montant': str(don.montant),
            'methode': don.methode,
            'date': don.date.isoformat(),
            'message': don.message
        })
    except Exception:
        return JsonResponse({'error': 'Don introuvable'}, status=404)
