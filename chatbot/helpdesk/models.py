

# Create your models here.
from django.db import models
from django.conf import settings

class Ticket(models.Model):
    STATUS_CHOICES = [
        ("new","Nuevo"),
        ("open","Abierto"),
        ("pending","Pendiente"),
        ("resolved","Resuelto"),
        ("closed","Cerrado"),
    ]
    title = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    external_contact = models.CharField(max_length=50, blank=True, null=True)  # número WhatsApp si no hay usuario
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"#{self.id} - {self.title} - {self.status}"

class Conversation(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="conversations", null=True, blank=True)
    contact = models.CharField(max_length=50)  # phone number (WhatsApp)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.CharField(max_length=50)  # 'user', 'agent', 'bot'
    text = models.TextField()
    raw_payload = models.JSONField(null=True, blank=True)  # almacenar raw webhook para reentrenamiento
    timestamp = models.DateTimeField(auto_now_add=True)
