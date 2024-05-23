from django import forms

class RegisterSummonerForm(forms.Form):
    summoner_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'yourGameName'}),
        required=True,
        max_length=30
    )
    
    tagline = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'yourTagLine'}),
        required=True,
        max_length=5
    )

    
