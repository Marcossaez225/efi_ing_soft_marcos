#users/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# Form for user registration
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    usable_password = None  # Ensures the password usability option is not displayed

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Disable the 'usable_password' option for frontend forms
        self.fields['password1'].widget.attrs['usable_password'] = None
        self.fields['password2'].widget.attrs['usable_password'] = None

    def clean_email(self):
        # Validate that the email is unique
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def clean_username(self):
        # Validate that the username is unique
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def save(self, commit=True):
        # Save the user instance with additional settings
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = False  # Ensure the user is not staff
        user.is_superuser = False  # Ensure the user is not a superuser
        if commit:
            user.save()
        return user

# Form for user login
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
