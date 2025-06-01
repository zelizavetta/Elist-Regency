from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Booking, Review
from django.forms import DateInput
from datetime import date


class DateTextInput(DateInput):
    input_type = 'text'       # вместо native date
    format     = '%Y-%m-%d'   # формат flatpickr

    def __init__(self, attrs=None, format=None):
        super().__init__(attrs=attrs, format=format or self.format)

class BookingForm(forms.ModelForm):
    check_in = forms.DateField(
        widget=DateTextInput(attrs={
            'autocomplete': 'off',
            'class': 'flatpickr',
            'placeholder': 'YYYY-MM-DD',
        }),
        input_formats=[
            '%Y-%m-%d',  # ISO, что выдаёт flatpickr
            '%m/%d/%Y',  # WebKit native (Chrome)
            '%d.%m.%Y',  # локали типа RU
        ],
        label='Дата заезда',
    )
    check_out = forms.DateField(
        widget=DateTextInput(attrs={
            'autocomplete': 'off',
            'class': 'flatpickr',
            'placeholder': 'YYYY-MM-DD',
        }),
        input_formats=[
            '%Y-%m-%d',
            '%m/%d/%Y',
            '%d.%m.%Y',
        ],
        label='Дата выезда',
    )

    class Meta:
        model  = Booking
        fields = ['check_in', 'check_out', 'guests', 'children']
        widgets = {
            'guests':   forms.HiddenInput(),
            'children': forms.HiddenInput(),
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
        fields = ['booking', 'rating', 'text']
        widgets = {
            'rating': forms.RadioSelect(),
            'text':   forms.Textarea(attrs={'rows':4}),
        }
        labels = {
            'rating': 'Ваша оценка',
            'text':   'Ваш отзыв',
        }


class CleaningForm(forms.Form):
    order_date = forms.DateField(
        label='Дата клининга',
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                # Эти атрибуты будут перезаписаны в __init__
                'min': date.today().isoformat(),
                'max': date.today().isoformat(),
            }
        )
    )
    order_time = forms.TimeField(
        label='Время клининга',
        widget=forms.TimeInput(attrs={'type': 'time'})
    )

    def __init__(self, *args, booking=None, **kwargs):
        """
        При создании формы обязательно передаём параметр booking=Booking(...)
        чтобы можно было валидировать дату относительно брони и задать min/max.
        """
        super().__init__(*args, **kwargs)
        self.booking = booking  # сохраняем для проверки в clean_order_date

        if booking:
            # Устанавливаем реальные границы для поля order_date
            self.fields['order_date'].widget.attrs['min'] = booking.check_in.isoformat()
            self.fields['order_date'].widget.attrs['max'] = booking.check_out.isoformat()

    def clean_order_date(self):
        od = self.cleaned_data.get('order_date')
        if not self.booking:
            return od  # без booking не проверяем

        # Проверяем, что дата клининга внутри периода проживания
        if od < self.booking.check_in or od > self.booking.check_out:
            raise forms.ValidationError("Пожалуйста, выберите дату клининга в пределах проживания (между датой заезда и датой выезда).")
        return od