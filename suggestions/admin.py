from django.contrib import admin
from suggestions.models import GiftCondition, GiftSuggestion

from django.contrib import admin
from suggestions.models import GiftCondition, GiftSuggestion

@admin.register(GiftCondition)
class GiftConditionAdmin(admin.ModelAdmin):
    list_display = ("gender", "relation", "age_group", "interest", "budget")
    list_filter = ("gender", "relation", "age_group", "interest", "budget")


@admin.register(GiftSuggestion)
class GiftSuggestionAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "get_gender",
        "get_relation",
        "get_age_group",
        "get_interest",
        "get_budget",
        "score",
    )
    search_fields = ("title", "description")
    list_filter = (
        "condition__gender",
        "condition__relation",
        "condition__age_group",
        "condition__interest",
        "condition__budget",
    )

    def get_gender(self, obj):
        return obj.condition.gender
    def get_relation(self, obj):
        return obj.condition.relation
    def get_age_group(self, obj):
        return obj.condition.age_group
    def get_interest(self, obj):
        return obj.condition.interest
    def get_budget(self, obj):
        return obj.condition.budget
