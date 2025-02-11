from django.shortcuts import get_object_or_404
from .models import *
from django import forms
import requests


class RiotAPIKeyForm(forms.Form):

    api_key = forms.CharField(max_length=100,
                              widget=forms.TextInput(attrs={'text': 'text', 'class':'form-control', 'id': 'inputText' }))
    
    def __init__(self, *args, **kwargs):
        admin = kwargs.pop('admin')
        super(RiotAPIKeyForm, self).__init__(*args, **kwargs)

        if admin:
            self.fields['api_key'].initial = admin.riot_api_key

    def clean_api_key(self):
        api_key = self.cleaned_data.get("api_key")
        url = "https://br1.api.riotgames.com/lol/status/v4/platform-data"
        headers = {"X-Riot-Token": api_key}
        response = requests.get(url, headers=headers)

        if response.status_code == 403:
            raise forms.ValidationError("Invalid or expired API key.")

        if response.status_code != 200:
            raise forms.ValidationError(f"Error validating the API key: {response.status_code}")

        return api_key