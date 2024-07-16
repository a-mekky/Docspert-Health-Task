import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Account
from .forms import UploadFileForm
from django.http import HttpResponse
from .forms import TransferForm
from django.db import transaction
from .importers import CSVImporter, JSONImporter


class UploadAccountsView(View):
    def get(self, request):
        form = UploadFileForm()
        return render(request, 'accounts/upload.html', {'form': form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                importer = CSVImporter()
            elif file.name.endswith('.json'):
                importer = JSONImporter()
            else:
                return HttpResponse('Unsupported file type', status=400)

            importer.import_data(file)
            return redirect('accounts:list')
        return render(request, 'accounts/upload.html', {'form': form})


class AccountListView(View):
    def get(self, request):
        accounts = Account.objects.all()
        return render(request, 'accounts/list.html', {'accounts': accounts})


class AccountDetailView(View):
    def get(self, request, account_id):
        account = get_object_or_404(Account, account_id=account_id)
        return render(request, 'accounts/detail.html', {'account': account})


class TransferFundsView(View):
    def get(self, request):
        form = TransferForm()
        return render(request, 'accounts/transfer.html', {'form': form})

    def post(self, request):
        form = TransferForm(request.POST)
        if form.is_valid():
            source_account = form.cleaned_data['source_account']
            destination_account = form.cleaned_data['destination_account']
            amount = form.cleaned_data['amount']

            try:
                with transaction.atomic():
                    source = source_account
                    destination = destination_account

                    if source.balance < amount:
                        return HttpResponse('Insufficient funds in the source account', status=400)

                    source.balance -= amount
                    destination.balance += amount
                    source.save()
                    destination.save()

                return redirect('accounts:list')
            except Account.DoesNotExist:
                return HttpResponse('One of the accounts does not exist', status=404)
        return render(request, 'accounts/transfer.html', {'form': form})


class UploadAccountsView(View):
    def get(self, request):
        form = UploadFileForm()
        return render(request, 'accounts/upload.html', {'form': form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.csv'):
                importer = CSVImporter()
            elif file.name.endswith('.json'):
                importer = JSONImporter()
            else:
                return HttpResponse('Unsupported file type', status=400)

            importer.import_data(file)
            return redirect('accounts:list')
        return render(request, 'accounts/upload.html', {'form': form})
