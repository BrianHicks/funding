from django.db import models

# Balanced Payments models
class BankAccount(models.Model):
    'represent a balanced bank account'
    name = models.CharField(max_length=100)
    uri = models.CharField(max_length=500)
