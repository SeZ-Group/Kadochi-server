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

# models.py

from django.db import models

TAG_CATEGORIES = [
    ("gender", "Gender"),
    ("relation", "Relation"),
    ("age_group", "Age Group"),
    ("budget", "Budget"),
    ("interest", "Interest"),
]

# تمام انتخاب‌های ممکن از همون Choiceهایی که قبلاً داشتی
TAG_VALUES = [
    # Gender
    ("male", "آقا"),
    ("female", "خانم"),
    # Relation
    ("friend", "دوست"),
    ("family", "خانواده"),
    ("partner", "پارتنر"),
    ("colleague", "همکار"),
    # Age
    ("teen", "نوجوان"),
    ("young", "جوان"),
    ("adult", "بزرگسال"),
    ("senior", "میانسال"),
    # Budget
    ("low", "کم"),
    ("medium", "متوسط"),
    ("high", "زیاد"),
    ("very_high", "خیلی زیاد"),
    # Interest
    ("tech", "تکنولوژی"),
    ("fashion", "مد"),
    ("art", "هنر"),
    ("books", "کتاب"),
    ("cooking", "آشپزی"),
    ("sports", "ورزش"),
    ("travel", "سفر"),
    ("gaming", "گیمینگ"),
    ("movies", "فیلم"),
]

class Tag(models.Model):
    category = models.CharField(max_length=50, choices=TAG_CATEGORIES)
    value = models.CharField(max_length=50, choices=TAG_VALUES)

    class Meta:
        unique_together = ("category", "value")

    def __str__(self):
        return dict(self._meta.get_field("value").choices).get(self.value, self.value)



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
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # اختیاری
    image_url = models.URLField(blank=True)     # اختیاری
    product_url = models.URLField(blank=True)   # اختیاری
    score = models.FloatField(default=0)
    price = models.FloatField(null=True, blank=True)  # ✅ جدید - قیمت
    active = models.BooleanField(default=True)        # ✅ جدید - فعال/غیرفعال
    tags = models.ManyToManyField('Tag', related_name="suggestions", blank=True)

    def __str__(self):
        return f"{self.title} (Score: {self.score})"
