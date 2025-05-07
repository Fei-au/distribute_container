# Create your views here.

import base64
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from pubsub.sub import save_messages
import os
import logging

subscriber_id = os.getenv('SUBSCRIBER_ID') 
logger = logging.getLogger('pubsub')

@csrf_exempt
def sub_push(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid method")
    try:
        envelope = json.loads(request.body)
        logger.info(json.dumps(envelope) if isinstance(envelope, dict) else envelope)
        message = envelope.get("message", {})
        logger.info(json.dumps(message) if isinstance(message, dict) else message)
        data = message.get("data")
        if data:
            decoded = base64.b64decode(data).decode("utf-8")
            logger.info(f"Pub/Sub message received")
            key = f'{subscriber_id}'
            save_messages(key, decoded)
        else:
            logger("Received message with no data")
        return JsonResponse({"status": "ok"})
    except Exception as e:
        logger(f"Error: {e}")
        return HttpResponseBadRequest("Error parsing Pub/Sub message")
