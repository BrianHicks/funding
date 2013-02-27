from django.db import models

# Balanced Payments models
class BankAccount(models.Model):
    'represent a balanced bank account'
    name = models.CharField(max_length=100)
    uri = models.CharField(max_length=500)

    class Meta:
        permissions = (
            ('view_bankaccount', 'View Bank Account'),
        )

    def __unicode__(self):
        return self.name
