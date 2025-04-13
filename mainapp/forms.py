from django import forms

class BookingForm(forms.Form):
    check_in = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'custom-date-input',}), label='Дата заезда')
    check_out = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'custom-date-input',}), label='Дата выезда')
    guests = forms.IntegerField(widget=forms.HiddenInput(), initial=1)
    children = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

class UserForm(forms.Form):
    name = forms.Field(widget=forms.TextInput(attrs={'type': 'text', 'class': 'custom-text-input',}), label="Имя")
    phone = forms.Field(widget=forms.TextInput(attrs={'type': 'text', 'class': 'custom-text-input',}), label="Номер телефона")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'type': 'email', 'class': 'custom-text-input',}), label="Email")
