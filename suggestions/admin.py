from django.contrib import admin

from suggestions.models import GiftSuggestion

# ADMIN
@admin.register(GiftSuggestion)
class GiftSuggestionAdmin(admin.ModelAdmin):
    list_display = ("title", "gender", "relation", "age_group", "interest", "budget")
    search_fields = ("title", "description")
    list_filter = ("gender", "relation", "age_group", "interest", "budget")
