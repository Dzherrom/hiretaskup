from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import Meeting

User = get_user_model()

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
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'input-field',
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'input-field',
            'autocomplete': 'new-password',
        })
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Identical email already exists.")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
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