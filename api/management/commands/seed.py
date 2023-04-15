import csv
from django.core.management.base import BaseCommand
import random
from django_seed import Seed
from main.models import Supply, Sale

MODE_REFRESH = 'refresh'
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = 'Loads data from a CSV file and populates the database using Django Seed.'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='api.file.csv')

    def handle(self, *args, **options):
        csv_file = options['csv_file']

        with open(csv_file, newline='') as f:
            reader = csv.DictReader(f)
            seeder = Seed.seeder()

            for row in reader:
                seeder.add_entity(Sale, 1, {
                    'id': row['column1'],
                    'barcode': row['column2'],
                    'quantity': row['column3'],
                    'price': row['column4'],
                    'sale_time': row['column5'],
                })

            seeder.execute()
