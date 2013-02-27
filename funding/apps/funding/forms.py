'forms for accounts'
from django import forms
from .models import BankAccount

class BankAccountForm(forms.ModelForm):
    'form for adding a bank account'
    class Meta:
        model = BankAccount
