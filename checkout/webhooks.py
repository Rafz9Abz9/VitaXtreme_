import json
from django.http import HttpResponse
import stripe
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from .webhook_handler import StripeWH_Handler


@require_POST
@csrf_exempt
def webhook(request):
    # Setup
    payload = request.body
    event = None
    wh_secret = settings.STRIPE_WH_SECRET
    stripe.api_key = settings.CLIENT_SECRET_KEY

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), wh_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    except Exception as e:
        # Invalid signature
        return HttpResponse(status=400)

    # setup a wh handler
    handler = StripeWH_Handler(request)

    #  Map webhook event with relevant handler function
    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
    }

    # Get the webhook type from stripe
    event_type = event['type']

    event_handler = event_map.get(event_type, handler.handle_event)

    # call event handler with the event
    response = event_handler(event)
    return response
