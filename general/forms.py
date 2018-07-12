from django import forms
from django.forms import ModelForm

from .models import *

class EventForm(ModelForm):
    class Meta:
        model = CoinEvent
        fields = '__all__'


class CoinLocaleForm(ModelForm):
    class Meta:
        model = CoinLocale
        fields = '__all__'
