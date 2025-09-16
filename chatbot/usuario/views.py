from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login

@api_view(["POST"])
def rut_login(request):
    rut = request.data.get("rut")
    password = request.data.get("password")
    user = authenticate(request, username=rut, password=password)  # si USERNAME_FIELD es rut
    if user:
        login(request, user)
        return Response({"status":"ok", "user_id": user.id})
    return Response({"error":"invalid_credentials"}, status=400)
