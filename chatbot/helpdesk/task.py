from celery import shared_task
from .models import Ticket
from .views import send_whatsapp_message

@shared_task
def send_ticket_reminder(ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if ticket.external_contact:
        send_whatsapp_message(ticket.external_contact, f"Recordatorio: su ticket #{ticket.id} aun está en estado {ticket.status}.")
