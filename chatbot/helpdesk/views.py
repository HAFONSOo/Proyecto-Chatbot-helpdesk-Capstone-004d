from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Ticket, Conversation, Message
from chatbot.services import ask_openai
import os, requests

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")  # Graph API token
WHATSAPP_PHONE_ID = os.getenv("WHATSAPP_PHONE_ID")
WHATSAPP_API = f"https://graph.facebook.com/v17.0/{WHATSAPP_PHONE_ID}/messages"

@csrf_exempt
@api_view(["GET","POST"])
def whatsapp_webhook(request):
    # GET: verification challenge (Facebook webhook)
    if request.method == "GET":
        mode = request.GET.get("hub.mode")
        token = request.GET.get("hub.verify_token")
        challenge = request.GET.get("hub.challenge")
        if mode == "subscribe" and token == os.getenv("WHATSAPP_VERIFY_TOKEN"):
            return Response(challenge)
        return Response("verification failed", status=403)

    payload = request.data  # JSON que envia WhatsApp
    # Simplificado: extraer sender y message
    try:
        # navegación de payload depende de la versión, ajustar según webhook real
        entry = payload.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])
        if not messages:
            return Response({"status":"no_messages"})
        msg = messages[0]
        sender = msg["from"]
        text = msg.get("text", {}).get("body", "")
    except Exception as e:
        return Response({"error":"invalid payload", "detail": str(e)} , status=400)

    # Guardar/recuperar conversación
    conv, _ = Conversation.objects.get_or_create(contact=sender)
    Message.objects.create(conversation=conv, sender="user", text=text, raw_payload=payload)

    # Lógica: determinar si crear ticket o responder con bot
    # Ejemplo: si el mensaje contiene "ayuda" -> crear ticket
    if "ticket" in text.lower() or "ayuda" in text.lower():
        ticket = Ticket.objects.create(title=text[:200], external_contact=sender, status="new")
        conv.ticket = ticket
        conv.save()
        reply = f"Gracias, he creado el ticket #{ticket.id}. Un agente te responderá pronto."
    else:
        # usar IA para responder automáticamente
        reply = ask_openai(prompt=f"Usuario: {text}\nResponde de forma breve y útil.")

    Message.objects.create(conversation=conv, sender="bot", text=reply)

    # Enviar respuesta por WhatsApp
    send_whatsapp_message(to=sender, text=reply)

    return Response({"status":"ok"})

def send_whatsapp_message(to, text):
    headers = {"Authorization": f"Bearer {WHATSAPP_TOKEN}", "Content-Type": "application/json"}
    data = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    r = requests.post(WHATSAPP_API, headers=headers, json=data)
    r.raise_for_status()
    return r.json()
