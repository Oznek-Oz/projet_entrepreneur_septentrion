from django.urls import path
from . import views

app_name = 'don'

urlpatterns = [
    path('', views.don, name='don'),
    path('cinetpay/init/<int:don_id>/', views.cinetpay_init, name='cinetpay_init'),
    path('cinetpay/return/', views.cinetpay_return, name='cinetpay_return'),
    path('cinetpay/notify/', views.cinetpay_notify, name='cinetpay_notify'),
    path('status/<int:don_id>/', views.don_status, name='don_status'),
] 