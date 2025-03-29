import csv
from django.core.management.base import BaseCommand
from suggestions.models import GiftSuggestion

class Command(BaseCommand):
    help = "Import gift suggestions from a CSV file."

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        file_path = options['csv_file']
        created, skipped = 0, 0

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = row.get('Title')
                if not title:
                    self.stdout.write(self.style.WARNING("Skipping row with missing title."))
                    skipped += 1
                    continue

                description = row.get('Description', '')
                image_url = row.get('Image URL', '')
                product_url = row.get('Product URL', '')
                price_str = row.get('Price', '').replace(',', '').strip()

                try:
                    price = float(price_str)
                except ValueError:
                    price = None

                suggestion = GiftSuggestion.objects.create(
                    title=title,
                    description=description,
                    image_url=image_url,
                    product_url=product_url,
                    price=price,
                    score=0,
                    active=True,
                )

                created += 1
                self.stdout.write(self.style.SUCCESS(f"Created suggestion: {suggestion.title}"))

        self.stdout.write(self.style.SUCCESS(f"✅ Done! {created} created, {skipped} skipped."))
