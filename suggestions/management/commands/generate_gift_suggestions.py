import os
import time
import json

from django.core.management.base import BaseCommand
from suggestions.models import (
    GiftCondition,
    GiftSuggestion,
    GENDER_CHOICES,
    AGE_GROUP_CHOICES,
    INTEREST_CHOICES,
    BUDGET_CHOICES,
)

from openai import OpenAI

# OpenAI client with optional base_url (for proxy server or relay)
client = OpenAI(
   api_key='',
   base_url=''
)


# Helper to get choice label
def get_label(choices, value):
    return dict(choices).get(value, value)

class Command(BaseCommand):
    help = "Generates gift suggestions using OpenAI (>=1.0.0) and saves them to the database."

    def handle(self, *args, **kwargs):
        conditions = GiftCondition.objects.all()
        total = len(conditions)
        count = 0

        for cond in conditions:
            count += 1
            self.stdout.write(f"[{count}/{total}] Generating for condition: {cond}")

            prompt = (
                f"من یک هدیه‌ای می‌خوام برای یک {get_label(GENDER_CHOICES, cond.gender)} هستش که تقریبا سنش "
                f"{get_label(AGE_GROUP_CHOICES, cond.age_group)} هست. به {get_label(INTEREST_CHOICES, cond.interest)} "
                f"علاقه داره و می‌خوام که اندازه {get_label(BUDGET_CHOICES, cond.budget)} هزینه کنم. "
                f"برام مهمه که تو ایران بتونم پیشنهادات رو پیدا کنم، مثلا از دی‌جی‌کالا یا ترب یا با سلام.\n\n"
                f"و دقیقا در این قالب جواب بهم بده:\n"
                f"[\n"
                f"    {{product-title: ..., product-image: ..., product-description: ..., product-url: ...}},\n"
                f"    ...\n"
                f"]"
            )

            self.stdout.write(prompt)

            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )

                reply = response.choices[0].message.content

                # سعی در پارس کردن JSON
                try:
                    # بعضی وقتا response ممکنه با ` ```json ` بیاد
                    reply_clean = reply.strip().removeprefix("```json").removesuffix("```").strip()
                    suggestions = json.loads(reply_clean.replace("'", '"'))
                except json.JSONDecodeError:
                    self.stdout.write(self.style.ERROR("❌ JSON parsing error"))
                    continue

                # حذف پیشنهادهای قبلی
                GiftSuggestion.objects.filter(condition=cond).delete()

                for s in suggestions:
                    GiftSuggestion.objects.create(
                        condition=cond,
                        title=s.get("product-title", "بدون عنوان"),
                        description=s.get("product-description", ""),
                        image_url=s.get("product-image", ""),
                        product_url=s.get("product-url", ""),
                        score=0  
                    )

                self.stdout.write(self.style.SUCCESS("✅ Suggestions saved."))

                time.sleep(2)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"🔥 Error: {str(e)}"))
