'forms for accounts'
from django import forms
from .models import BalancedAccount

class BalancedAccountForm(forms.ModelForm):
    'form for adding a bank account'
    class Meta:
        model = BalancedAccount
