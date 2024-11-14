from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

# Formulario de registro de usuario
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label=_("Email"))
    usable_password = None  # Asegura que la opción de usabilidad de contraseña no se muestre

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': _("Username"),
            'password1': _("Password"),
            'password2': _("Confirm Password"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Deshabilita la opción de 'usable_password' para el frontend
        self.fields['password1'].widget.attrs['usable_password'] = None
        self.fields['password2'].widget.attrs['usable_password'] = None

    def clean_email(self):
        # Validar que el email sea único
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("A user with this email already exists."))
        return email

    def clean_username(self):
        # Validar que el username sea único
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("This username is already taken."))
        return username

    def save(self, commit=True):
        # Guardar el usuario con configuraciones adicionales
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = False  # Asegura que el usuario no sea staff
        user.is_superuser = False  # Asegura que el usuario no sea superusuario
        if commit:
            user.save()
        return user

# Formulario de login de usuario
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
