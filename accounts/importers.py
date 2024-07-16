from abc import ABC, abstractmethod
import csv
import json
from .models import Account


class BaseImporter(ABC):
    @abstractmethod
    def import_data(self, file):
        pass


class CSVImporter(BaseImporter):
    def import_data(self, file):
        decoded_file = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        for row in reader:
            Account.objects.update_or_create(
                account_id=row['ID'],
                defaults={'account_name': row['Name'], 'balance': row['Balance']}
            )


class JSONImporter(BaseImporter):
    def import_data(self, file):
        data = json.load(file)
        for row in data:
            Account.objects.update_or_create(
                account_id=row['ID'],
                defaults={'account_name': row['Name'], 'balance': row['Balance']}
            )

