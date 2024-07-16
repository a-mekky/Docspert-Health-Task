from django import forms
from .models import Account


class UploadFileForm(forms.Form):
    file = forms.FileField()


class TransferForm(forms.Form):
    source_account = forms.ModelChoiceField(queryset=Account.objects.all(), label="Source Account")
    destination_account = forms.ModelChoiceField(queryset=Account.objects.all(), label="Destination Account")
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
