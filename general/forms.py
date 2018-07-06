from django import forms
from django.forms import ModelForm

from .models import *

class EventForm(ModelForm):
    class Meta:
        model = CoinEvent
        fields = '__all__'
