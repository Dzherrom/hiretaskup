from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import CustomUser

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password'] 

PAIS_CHOICES = [
    ('', 'Select a country'),
    ('AR', 'Argentina'),
    ('BR', 'Brazil'),
    ('CL', 'Chile'),
    ('CO', 'Colombia'),
    ('MX', 'Mexico'),
    ('PE', 'Peru'),
    ('UY', 'Uruguay'),
]

class ProfileForm(forms.ModelForm):
    country = forms.ChoiceField(choices=PAIS_CHOICES, required=True, label="Country")
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='Password')
    verify_password = forms.CharField(widget=forms.PasswordInput, required=False, label='Verify')

    class Meta:
        model = CustomUser
        fields = [
            'country', 'username', 'email', 'phone_number', 'first_name', 'last_name', 'address','website', 'photo', 'password', 'verify_password'
        ]
        widgets = {
            'address': forms.TextInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        verify_password = cleaned_data.get("verify_password")
        if password and password != verify_password:
            self.add_error('verify_password', "Passwords do not match.")
    
    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        country = self.cleaned_data.get('country')
        phone_lengths = {'co': 10, 'mx': 10, 'ar': 10}
        if not phone.isdigit():
            raise forms.ValidationError("Solo se permiten números.")
        if country and len(phone) != phone_lengths.get(country, 10):
            raise forms.ValidationError(f"El número debe tener {phone_lengths.get(country, 10)} dígitos.")
        return phone