from django.core.management.base import BaseCommand
from itertools import product
from suggestions.models import GiftCondition
from suggestions.models import GENDER_CHOICES, RELATION_CHOICES, AGE_GROUP_CHOICES, BUDGET_CHOICES, INTEREST_CHOICES

class Command(BaseCommand):
    help = "Populate the database with all combinations of GiftCondition."

    def handle(self, *args, **options):
        genders = [g[0] for g in GENDER_CHOICES]
        # relations = [r[0] for r in RELATION_CHOICES]
        age_groups = [a[0] for a in AGE_GROUP_CHOICES]
        budgets = [b[0] for b in BUDGET_CHOICES]
        interests = [i[0] for i in INTEREST_CHOICES]

        all_combinations = list(product(genders, age_groups, budgets, interests))

        created = 0
        skipped = 0

        for gender, age_group, budget, interest in all_combinations:
            obj, created_flag = GiftCondition.objects.get_or_create(
                gender=gender,
                # relation=relation,
                age_group=age_group,
                budget=budget,
                interest=interest
            )
            if created_flag:
                created += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(f"✅ Created: {created}, ❗ Skipped (already exists): {skipped}"))
