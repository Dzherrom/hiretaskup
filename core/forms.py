from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
import re
from .models import Meeting

User = get_user_model()

# Validadores Estrictos
name_validator = RegexValidator(
    regex=r'^[a-zA-Z\s]+$',
    message='El nombre solo debe contener letras.'
)
phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message='Ingrese un número de teléfono válido (ej: +1234567890).'
)


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username',
            'class': 'input-field',
            'autocomplete': 'username',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email',
            'class': 'input-field',
            'autocomplete': 'email',
        })
        # Note: password fields in UserCreationForm are usually handled by the parent class in a specific way,
        # but if we want to add attributes via init, we access them if they exist in self.fields.
        # UserCreationForm uses 'password_1' and 'password_2' or similar depending on Django version? 
        # Actually standard Django UserCreationForm uses 'username', 'password1', 'password2'.
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'placeholder': 'Password',
                'class': 'input-field',
                'autocomplete': 'new-password',
            })
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'placeholder': 'Confirm Password',
                'class': 'input-field',
                'autocomplete': 'new-password',
            })

    # Validación estricta de correo único
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class ContactForm(forms.Form):
    name = forms.CharField(validators=[name_validator], max_length=100)
    # Acepta email o teléfono validando el formato
    contact_info = forms.CharField(max_length=100)
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea, max_length=500, help_text="Maximum 500 characters") # Rate Limiting: Max length

    def clean_contact_info(self):
        data = self.cleaned_data.get('contact_info')
        # Validar si es email o teléfono válido
        is_email = False
        is_phone = False
        
        try:
            EmailValidator()(data)
            is_email = True
        except ValidationError:
            pass
            
        if re.match(r'^\+?1?\d{9,15}$', data):
            is_phone = True
            
        if not (is_email or is_phone):
            raise ValidationError("Ingrese un email válido o un número de teléfono válido.")
        return data

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username',
            'class': 'input-field',
            'autocomplete': 'username',
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'input-field',
            'autocomplete': 'current-password',
        })
    class Meta:
        model = User
        fields = ['username', 'password'] 
        
class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['name', 'email', 'guests', 'important', 'phone', 'date', 'time', 'timezone']

# Checkout Form
class CheckoutForm(forms.Form):
    plan_id = forms.IntegerField(widget=forms.HiddenInput())
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.HiddenInput())
    timezone = forms.CharField(widget=forms.HiddenInput(), required=False) # Will be populated by JS
    
    # User Details (Prefilled or editable)
    full_name = forms.CharField(max_length=150)
    business_name = forms.CharField(max_length=150, required=False)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False)
    website = forms.URLField(required=False)
    
    # Onboarding questions
    company_type = forms.CharField(max_length=100, required=False)
    client_needs = forms.CharField(widget=forms.Textarea, required=False)
    va_tasks = forms.CharField(widget=forms.Textarea, required=False)

# Formularios para OTP (Recuperación de contraseña)
class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("No existe un usuario con este correo.")
        return email

class PasswordResetVerifyForm(forms.Form):
    otp = forms.CharField(min_length=6, max_length=6, widget=forms.TextInput(attrs={'placeholder': 'Código de 6 dígitos'}))
    new_password = forms.CharField(widget=forms.PasswordInput, min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('new_password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            raise ValidationError("Las contraseñas no coinciden.")
        return cleaned_data