from django.db import models

GENDER_CHOICES = [
    ("male", "مرد"),
    ("female", "زن"),
]

RELATION_CHOICES = [
    ("friend", "یک دوست صمیمی"),
    ("family", "یکی از اعضای خانواده"),
    ("partner", "یک پارتنر عاشقانه"),
    ("colleague", "یک همکار یا آشنا"),
]

AGE_GROUP_CHOICES = [
    ("teen", "نوجوان (۱۰ تا ۱۸ سال)"),
    ("young", "جوان (۱۸ تا ۳۵ سال)"),
    ("adult", "بزرگسال (۳۵ تا ۵۰ سال)"),
    ("senior", "میانسال یا مسن (۵۱ سال به بالا)"),
]

BUDGET_CHOICES = [
    ("low", "کمتر از ۱۰۰ هزار تومان"),
    ("medium", "بین ۱۰۰ هزار تا ۱ میلیون تومان"),
    ("high", "بین ۱ تا ۵ میلیون تومان"),
    ("very_high", "بیشتر از ۵ میلیون تومان"),
]

INTEREST_CHOICES = [
    ("tech", "تکنولوژی و گجت‌ها"),
    ("fashion", "مد و استایل"),
    ("art", "هنر"),
    ("books", "کتاب و مطالعه"),
    ("cooking", "آشپزی و غذا"),
    ("sports", "ورزش"),
    ("travel", "سفر و ماجراجویی"),
    ("gaming", "بازی و گیمینگ"),
    ("movies", "فیلم و سریال"),
]

# --- GiftCondition Model ---
class GiftCondition(models.Model):
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    relation = models.CharField(max_length=50, choices=RELATION_CHOICES)
    age_group = models.CharField(max_length=50, choices=AGE_GROUP_CHOICES)
    budget = models.CharField(max_length=50, choices=BUDGET_CHOICES)
    interest = models.CharField(max_length=50, choices=INTEREST_CHOICES)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["gender", "relation", "age_group", "budget", "interest"],
                name="unique_condition"
            )
        ]

    def __str__(self):
        return f"{self.gender} - {self.relation} - {self.age_group} - {self.budget} - {self.interest}"


class GiftSuggestion(models.Model):
    condition = models.ForeignKey(GiftCondition, related_name='suggestions', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField()
    product_url = models.URLField()
    score = models.FloatField()

    def as_dict(self):
        return {
            "product-title": self.title,
            "product-description": self.description,
            "product-image": self.image_url,
            "product_url": self.product_url,
            "score": self.score,
        }

    def __str__(self):
        return f"{self.title} (Score: {self.score})"
