from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Meeting

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password'] 
        
class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['name', 'email', 'guests', 'important', 'phone', 'date', 'time', 'timezone']