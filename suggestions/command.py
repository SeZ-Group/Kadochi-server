import csv
from django.core.management.base import BaseCommand
from suggestions.models import GiftSuggestion


# MANAGEMENT COMMAND TO IMPORT CSV DATA
class Command(BaseCommand):
    help = 'Import gift suggestions from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                GiftSuggestion.objects.create(
                    gender=row['gender'],
                    relation=row['relation'],
                    age_group=row['age_group'],
                    interest=row['interest'],
                    budget=row['budget'],
                    title=row['title'],
                    description=row['description'],
                    image_url=row['image_url'],
                    product_url=row['product_url']
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully imported {count} suggestions'))