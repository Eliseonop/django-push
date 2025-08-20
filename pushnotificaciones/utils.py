from pywebpush import webpush, WebPushException
from .models import Subscription

VAPID_PRIVATE_KEY = "TU_PRIVATE_VAPID_KEY"
VAPID_CLAIMS = {"sub": "mailto:tu@email.com"}

def send_notification(payload):
    for sub in Subscription.objects.all():
        try:
            webpush(
                subscription_info={"endpoint": sub.endpoint, "keys": sub.keys},
                data=payload,
                vapid_private_key=VAPID_PRIVATE_KEY,
                vapid_claims=VAPID_CLAIMS
            )
        except WebPushException as ex:
            print("Error enviando:", repr(ex))
