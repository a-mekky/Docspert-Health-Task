from django.db import models

class Account(models.Model):
    account_id = models.CharField(max_length=20, unique=True)
    account_name = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.account_name} ({self.account_id})"
