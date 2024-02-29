from django.shortcuts import get_object_or_404
from .models import *
from django import forms


class RiotAPIKeyForm(forms.Form):

    api_key = forms.CharField(max_length=100,
                              widget=forms.TextInput(attrs={'text': 'text', 'class':'form-control', 'id': 'inputText' }))
    
    def __init__(self, *args, **kwargs):
        admin = kwargs.pop('admin')
        super(RiotAPIKeyForm, self).__init__(*args, **kwargs)

        if admin:
            self.fields['api_key'].initial = admin.riot_api_key