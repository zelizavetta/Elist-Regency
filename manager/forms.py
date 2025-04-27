from django import forms
from mainapp.models import Dish, Room


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ['restaurant', 'name', 'description', 'price', 'image']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['number', 'room_type', 'price', 'image']
        widgets = {
            'room_type': forms.Select(),
            'price':     forms.NumberInput(attrs={'step': '0.01'}),
        }