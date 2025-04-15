from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile


class BookingForm(forms.Form):
    check_in = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'custom-date-input',}), label='Дата заезда')
    check_out = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'custom-date-input',}), label='Дата выезда')
    guests = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    children = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'phone', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'custom-text-input', 'placeholder': 'Введите имя'}),
            'phone': forms.TextInput(attrs={'class': 'custom-text-input', 'placeholder': 'Введите номер телефона'}),
            'email': forms.EmailInput(attrs={'class': 'custom-text-input', 'placeholder': 'Введите email'}),
        }
        labels = {
            'name': 'Имя',
            'phone': 'Номер телефона',
            'email': 'Email',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Если email пустой, возвращаем None, чтобы в базе сохранялось NULL
        if email == '':
            return None
        return email


# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'custom-text-input'})
    )
    
    class Meta:
        model = User  # Используем модель User, а не UserProfile
        fields = ("username", "email", "password1", "password2")
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
