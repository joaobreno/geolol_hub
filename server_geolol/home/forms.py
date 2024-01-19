from django import forms
import re

# class LoginForm(forms.Form):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'yourUsername'}),
#                                required=True)
    
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'yourPassword'}),
#                                required=True)
    
#     remember_me = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'rememberMe'}),
#                                   required=False)
    
#     def clean_username(self):
#         data = data = self.cleaned_data['username']
#         if not re.match(r'^[a-zA-Z0-9_]+$', data):
#             raise forms.ValidationError("Usuário não pode conter caracteres especiais!")
