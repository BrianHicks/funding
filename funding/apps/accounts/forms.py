'forms for accounts'
from django import forms

class ReceiverAddAccountForm(forms.Form):
    'form for adding an account as a receiver'
    name = forms.CharField()
