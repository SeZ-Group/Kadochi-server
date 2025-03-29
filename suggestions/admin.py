# admin.py

from django.contrib import admin
from .models import GiftSuggestion, Tag

# suggestions/admin.py

from django import forms
from django.contrib import admin
from .models import GiftSuggestion, Tag

class GiftSuggestionAdminForm(forms.ModelForm):
    gender_tag = forms.ModelChoiceField(
        queryset=Tag.objects.filter(category='gender'),
        required=False,
        label="جنسیت"
    )
    relation_tag = forms.ModelChoiceField(
        queryset=Tag.objects.filter(category='relation'),
        required=False,
        label="نسبت"
    )
    age_group_tag = forms.ModelChoiceField(
        queryset=Tag.objects.filter(category='age_group'),
        required=False,
        label="گروه سنی"
    )
    budget_tag = forms.ModelChoiceField(
        queryset=Tag.objects.filter(category='budget'),
        required=False,
        label="بودجه"
    )
    interest_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(category='interest'),
        required=False,
        label="علاقه‌مندی‌ها",
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = GiftSuggestion
        fields = ['title', 'description', 'image_url', 'product_url', 'score']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # پیش‌فرض‌ها (برای حالت ویرایش)
        if self.instance.pk:
            tags = self.instance.tags.all()
            self.fields['gender_tag'].initial = tags.filter(category='gender').first()
            self.fields['relation_tag'].initial = tags.filter(category='relation').first()
            self.fields['age_group_tag'].initial = tags.filter(category='age_group').first()
            self.fields['budget_tag'].initial = tags.filter(category='budget').first()
            self.fields['interest_tags'].initial = tags.filter(category='interest')

    def save(self, commit=True):
        instance = super().save(commit=False)

        # حتماً شیء رو ذخیره می‌کنیم (تا ID بگیره)
        instance.save()

        # تگ‌ها رو جمع می‌کنیم
        selected_tags = [
            self.cleaned_data.get('gender_tag'),
            self.cleaned_data.get('relation_tag'),
            self.cleaned_data.get('age_group_tag'),
            self.cleaned_data.get('budget_tag'),
        ]
        selected_tags = [tag for tag in selected_tags if tag]  # حذف None
        selected_tags += list(self.cleaned_data.get('interest_tags', []))

        # ست کردن تگ‌ها
        instance.tags.set(selected_tags)

        return instance




# تگ‌ها رو بشه فیلتر کرد و راحت انتخاب کرد
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('category', 'value')
    list_filter = ('category',)
    search_fields = ('value',)


@admin.register(GiftSuggestion)
class GiftSuggestionAdmin(admin.ModelAdmin):
    form = GiftSuggestionAdminForm
    list_display = ('title', 'score')
    search_fields = ('title', 'description')
