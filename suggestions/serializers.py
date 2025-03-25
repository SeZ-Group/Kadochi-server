from rest_framework import serializers
from suggestions.models import GiftCondition, GiftSuggestion

class GiftSuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftSuggestion
        fields = ['id', 'title', 'description', 'image_url', 'product_url', 'score']

class GiftConditionSerializer(serializers.ModelSerializer):
    suggestions = GiftSuggestionSerializer(many=True, read_only=True)

    class Meta:
        model = GiftCondition
        fields = '__all__'
