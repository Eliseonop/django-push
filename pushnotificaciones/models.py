from django.db import models

class PushSubscription(models.Model):
    """
    Model to store FCM tokens (formerly WebPush subscriptions)
    """
    token = models.CharField(max_length=500, unique=True)  # ahora almacenamos el token FCM
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FCM Token {self.id} - {self.token[:50]}..."
