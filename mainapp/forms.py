from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Booking, Review


class DateTextInput(forms.DateInput):
    input_type = 'text'   # вместо 'date'

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'guests', 'children']
        widgets = {
            'check_in': DateTextInput(attrs={'class': 'custom-date-input'}),
            'check_out': DateTextInput(attrs={'class': 'custom-date-input'}),
            'guests': forms.HiddenInput(),
            'children': forms.HiddenInput(),
        }
        labels = {
            'check_in': 'Дата заезда',
            'check_out': 'Дата выезда',
        }


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

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.RadioSelect(),
            'text':   forms.Textarea(attrs={'rows':4}),
        }
        labels = {
            'rating': 'Ваша оценка',
            'text':   'Ваш отзыв',
        }


