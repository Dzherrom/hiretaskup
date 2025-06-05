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

class ProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=False, label='Password')
    verify_password = forms.CharField(widget=forms.PasswordInput, required=False, label='Verify')

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'phone_number', 'first_name', 'last_name', 'address','photo', 'password', 'verify_password'
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