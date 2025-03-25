from django.contrib import admin
from suggestions.models import GiftCondition, GiftSuggestion

from django.contrib import admin
from suggestions.models import GiftCondition, GiftSuggestion
from .forms import GiftConditionForm  # فرض بر اینکه فایلش توی forms.py هست

@admin.register(GiftCondition)
class GiftConditionAdmin(admin.ModelAdmin):
    form = GiftConditionForm  # 🔥 این مهم‌ترین خطه
    list_display = ("gender", "relation", "age_group", "get_interests", "budget")
    list_filter = ("gender", "relation", "age_group", "budget")

    def get_interests(self, obj):
        return ", ".join(obj.interests)
    get_interests.short_description = "Interests"


@admin.register(GiftSuggestion)
class GiftSuggestionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "get_gender",
        "get_relation",
        "get_age_group",
        "get_interests",
        "get_budget",
        "score",
    )
    search_fields = ("title", "description")
    list_filter = (
        "condition__gender",
        "condition__relation",
        "condition__age_group",
        "condition__budget",  # حذف condition__interest
    )

    def get_gender(self, obj):
        return obj.condition.gender
    def get_relation(self, obj):
        return obj.condition.relation
    def get_age_group(self, obj):
        return obj.condition.age_group
    def get_budget(self, obj):
        return obj.condition.budget

    def get_interests(self, obj):
        return ", ".join(obj.condition.interests)
    get_interests.short_description = 'Interests'
