from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from decimal import Decimal
from .models import Account
from .importers import JSONImporter,CSVImporter
import json
import csv


class AccountModelTests(TestCase):

    def setUp(self):
        # Set up initial data if needed
        pass

    def test_import_from_csv(self):
        csv_data = """ID,Name,Balance
cc26b56c-36f6-41f1-b689-d1d5065b95af,Joy Dean,4497.22
be6acfdc-cae1-4611-b3b2-dfb5167ba5fe,Bryan Rice,2632.76
43caa0b8-76a4-4e61-b7c3-f2f5ee4b4f77,Ms. Jamie Lopez,1827.85
69c93967-e20f-4735-9b8d-1b7dd56340ab,Lauren David,9778.7
60c233f0-1bfa-4f00-b1b3-5b6443c2670e,Gregory Elliott,1926.39
07414d78-ea39-46c3-a653-bd9c35381846,Ellen Miranda,785.83
9f43a9f5-65d8-4d71-a8e5-16e7c565173e,Joseph Krause,3096.18
270a774f-bb53-4101-b071-8e6111606911,Christina Mcintosh,6130.67
"""
        file = SimpleUploadedFile("accounts.csv", csv_data.encode(), content_type="text/csv")
        importer = CSVImporter()
        importer.import_data(file)

        self.assertEqual(Account.objects.count(), 8)
        account = Account.objects.get(account_id="cc26b56c-36f6-41f1-b689-d1d5065b95af")
        self.assertEqual(account.account_name, "Joy Dean")
        self.assertEqual(account.balance, Decimal('4497.22'))

    def test_import_from_json(self):
        json_data = [
            {
                "ID": "cc26b56c-36f6-41f1-b689-d1d5065b95af",
                "Name": "Joy Dean",
                "Balance": 4497.22
            },
            {
                "ID": "be6acfdc-cae1-4611-b3b2-dfb5167ba5fe",
                "Name": "Bryan Rice",
                "Balance": 2632.76
            },
            {
                "ID": "43caa0b8-76a4-4e61-b7c3-f2f5ee4b4f77",
                "Name": "Ms. Jamie Lopez",
                "Balance": 1827.85
            },
            {
                "ID": "69c93967-e20f-4735-9b8d-1b7dd56340ab",
                "Name": "Lauren David",
                "Balance": 9778.7
            },
            {
                "ID": "60c233f0-1bfa-4f00-b1b3-5b6443c2670e",
                "Name": "Gregory Elliott",
                "Balance": 1926.39
            },
            {
                "ID": "07414d78-ea39-46c3-a653-bd9c35381846",
                "Name": "Ellen Miranda",
                "Balance": 785.83
            },
            {
                "ID": "9f43a9f5-65d8-4d71-a8e5-16e7c565173e",
                "Name": "Joseph Krause",
                "Balance": 3096.18
            },
            {
                "ID": "270a774f-bb53-4101-b071-8e6111606911",
                "Name": "Christina Mcintosh",
                "Balance": 6130.67
            },
        ]
        file = SimpleUploadedFile("accounts.json", json.dumps(json_data).encode(), content_type="application/json")
        importer = JSONImporter()
        importer.import_data(file)

        self.assertEqual(Account.objects.count(), 8)
        account = Account.objects.get(account_id="cc26b56c-36f6-41f1-b689-d1d5065b95af")
        self.assertEqual(account.account_name, "Joy Dean")
        self.assertEqual(account.balance, Decimal('4497.22'))

    def test_transfer_funds(self):
        # Create test accounts
        Account.objects.create(account_id="1", account_name="Account 1", balance=Decimal('1000.00'))
        Account.objects.create(account_id="2", account_name="Account 2", balance=Decimal('500.00'))

        source_account = Account.objects.get(account_id="1")
        destination_account = Account.objects.get(account_id="2")

        amount = Decimal('200.00')

        with transaction.atomic():
            source_account.balance -= amount
            destination_account.balance += amount
            source_account.save()
            destination_account.save()

        source_account.refresh_from_db()
        destination_account.refresh_from_db()

        self.assertEqual(source_account.balance, Decimal('800.00'))
        self.assertEqual(destination_account.balance, Decimal('700.00'))
