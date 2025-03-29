# suggestions/management/commands/create_standard_tags.py

from django.core.management.base import BaseCommand
from suggestions.models import Tag

class Command(BaseCommand):
    help = "Creates all standard tags for gift suggestions"

    TAG_DATA = {
        "gender": ["male", "female"],
        "relation": ["friend", "family", "partner", "colleague"],
        "age_group": ["teen", "young", "adult", "senior"],
        "budget": ["low", "medium", "high", "very_high"],
        "interest": ["tech", "fashion", "art", "books", "cooking", "sports", "travel", "gaming", "movies"],
    }

    def handle(self, *args, **kwargs):
        created, skipped = 0, 0

        for category, values in self.TAG_DATA.items():
            for value in values:
                obj, was_created = Tag.objects.get_or_create(category=category, value=value)
                if was_created:
                    created += 1
                else:
                    skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f"✅ Done! {created} tags created, {skipped} already existed."
        ))
