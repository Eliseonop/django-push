from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import PushSubscription
from firebase_admin import messaging,exceptions


@csrf_exempt
@require_http_methods(["POST"])
def save_subscription(request):
    try:
        data = json.loads(request.body)
        token = data.get('token')

        if not token:
            return JsonResponse({'success': False, 'error': 'No token provided'})

        subscription, created = PushSubscription.objects.get_or_create(token=token)

        return JsonResponse({
            'success': True,
            'message': 'FCM token saved successfully',
            'created': created
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


@csrf_exempt
@require_http_methods(["POST"])
def send_notification(request):
    try:
        data = json.loads(request.body)

        # Detectar formato y extraer datos
        if 'data' in data and isinstance(data['data'], dict):
            ticket_data = data['data']
            title = data.get('title', ticket_data.get('asunto', 'Nuevo ticket'))
            body = data.get('body', '')
            ticket_id = str(ticket_data.get('ticket_id', '0'))
            descripcion = ticket_data.get('descripcion', '')
            asignado_a = ticket_data.get('asignado_a', {})
            creado_por = ticket_data.get('creado_por', {})
            asunto = ticket_data.get('asunto', title)
        else:
            ticket_id = str(data.get('id', '0'))
            title = data.get('asunto', 'Nuevo ticket')
            creado_por = data.get('creado_por', {})
            asignado_a = data.get('asignado_a', {})
            descripcion = data.get('descripcion', '')
            asunto = title
            body = data.get(
                'body') or f"Creado por: {creado_por.get('nombre', '')}\nAsignado a: {asignado_a.get('nombre', '')}"

        subscriptions = PushSubscription.objects.all()
        sent_count = failed_count = 0

        for sub in subscriptions:
            try:
                # SOLO data, SIN notification para evitar doble notificación
                message = messaging.Message(
                    data={
                        "ticket_id": ticket_id,
                        "title": title,  # Se mueve a data
                        "body": body,  # Se mueve a data
                        "descripcion": json.dumps(descripcion) if descripcion else "",
                        "asunto": json.dumps(asunto) if asunto else "",
                        "asignado_a": json.dumps(asignado_a) if asignado_a else "{}",
                        "creado_por": json.dumps(creado_por) if creado_por else "{}"
                    },
                    token=sub.token
                )

                response = messaging.send(message)
                print(f"FCM notification sent: {response}")
                sent_count += 1


            except exceptions.FirebaseError as ex:

                print(f"⚠️ Error FCM: {type(ex).__name__} - {getattr(ex, 'code', '')} - {str(ex)}")


                if ex.code in ["messaging/invalid-argument",

                               "messaging/invalid-registration-token",

                               "messaging/registration-token-not-registered"]:
                    print(f"🗑️ Eliminando token inválido: {sub.token[:20]}...")

                    sub.delete()

                failed_count += 1


            except Exception as ex:

                print(f"❌ Error inesperado con token {sub.token[:20]}...: {ex}")

                failed_count += 1

        return JsonResponse({
            'success': True,
            'sent': sent_count,
            'failed': failed_count,
            'total_subscriptions': subscriptions.count(),
            'message': f'Notifications processed: {sent_count} sent, {failed_count} failed'
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON in request body'})
    except Exception as e:
        print(f"Error in send_notification: {e}")
        return JsonResponse({'success': False, 'error': str(e)})