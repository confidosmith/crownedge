from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from .models import Profile


class SignupForm(UserCreationForm):
    username = forms.CharField(max_length=20, required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=50, required=True)

    class Meta:
        model = User 
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


STATE = [
    ('Abia', 'Abia'),
    ('Bayelsa', 'Bayelsa'),
    ('Delta', 'Delta'),
    ('Edo', 'Edo'),
    ('Enugu', 'Enugu'),
    ('Gombe', 'Gombe'),
    ('Kaduna', 'Kaduna'),
    ('Lagos', 'Lagos'),
    ('Taraba', 'Taraba'),
]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['id', 'first_name', 'last_name', 'phone', 'state', 'address', 'pix']
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Last name'}),
            'phone': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Phone'}),
            'state': forms.Select(attrs={'class':'form-control', 'placeholder': 'State'}, choices=STATE),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Address'}),
            'pix': forms.FileInput(attrs={'class':'form-control', 'placeholder': 'Upload Image'}),
        }