from django.shortcuts import render,redirect
from .forms import FormularioIniciar
from django.contrib.auth import authenticate, login ,logout

def ver_iniciar(request):
    if request.user.is_authenticated:
        return redirect('principal')
    if request.method == 'GET':
        contexto = {
            'formulario':FormularioIniciar(),
        }
        return render(request,'chatbot/chatbot.html',contexto)
    if request.method == 'POST':
        datos_usuario = FormularioIniciar(data = request.POST)
        es_valido = datos_usuario.is_valid()
        if es_valido:
            usuario = authenticate(
                username = datos_usuario.cleaned_data['usuario'],
                password = datos_usuario.cleaned_data['contrasena']
            )
            if usuario is not None:
                login(request, usuario)
                success(request, f'Bienvenido {usuario.username}')
                return redirect('principal')
            msg_error='Error en usuario o contraseña'
                
        warning(request, 'Usuario y/o contraseña invalido(s) :(')
        contexto = {
            'formulario': datos_usuario,
            'msg_error':msg_error
    
        }
        return render(request,'chatbot/chatbot.html',contexto)
def fun_cerrar(request):
    if request.user.is_authenticated:
        logout(request)
        success(request, 'Sesión cerrada ')
    return redirect('')