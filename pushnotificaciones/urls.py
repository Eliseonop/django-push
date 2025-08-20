from django.urls import path
from . import views

urlpatterns = [
    path('save-subscription/', views.save_subscription, name='save_subscription'),
    path('enviar-notificacion/', views.send_notification, name='send_notification'),
]

