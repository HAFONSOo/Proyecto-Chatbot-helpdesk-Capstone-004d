from django.forms import (
    Form,
    CharField,
    PasswordInput,
    EmailInput,
    TextInput
)

from django.contrib.auth.models import User
class FormularioIniciar(Form):
    usuario = CharField(
        required = True,
        label = 'Ingrese su usuario',
        widget = TextInput(
            attrs = {
                'class':'form-control rounded-5 shadow text-center',
                'placeholder':'Usuario'
            }
        )
    )
    contrasena = CharField(
        required = True,
        min_length = 4,
        max_length = 16,
        label = 'Ingrese su contraseña',
        widget = PasswordInput(
            attrs = {
                'class':'form-control rounded-5 shadow text-center',
                'placeholder':'Contraseña'
            }
        )
    )