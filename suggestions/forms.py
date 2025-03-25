from django import forms
from suggestions.models import GiftCondition, INTEREST_CHOICES

class GiftConditionForm(forms.ModelForm):
    interests = forms.MultipleChoiceField(
        choices=INTEREST_CHOICES,
        widget=forms.CheckboxSelectMultiple, 
        required=False
    )

    class Meta:
        model = GiftCondition
        fields = '__all__'
