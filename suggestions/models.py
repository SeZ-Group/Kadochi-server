from django.db import models

# MODELS
class GiftSuggestion(models.Model):
    gender = models.CharField(max_length=50)
    relation = models.CharField(max_length=50)
    age_group = models.CharField(max_length=50)
    interest = models.CharField(max_length=50)
    budget = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image_url = models.URLField()
    product_url = models.URLField()

    def as_dict(self):
        return {
            "product-title": self.title,
            "product-description": self.description,
            "product-image": self.image_url,
            "product_url": self.product_url,
        }

    def __str__(self):
        return f"{self.title} ({self.gender}, {self.relation}, {self.age_group})"
