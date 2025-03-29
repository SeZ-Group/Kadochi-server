from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from suggestions.models import GiftCondition
from .serializers import GiftSuggestionSerializer
import random
from suggestions.models import GiftSuggestion
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from suggestions.models import GiftSuggestion, Tag
from .serializers import GiftSuggestionSerializer

class SuggestionAPI(APIView):
    def post(self, request):
        data = request.data
        print('api called, ', data)

        gender = data.get('gender')
        age_group = data.get('age_group')
        interests = data.get('interest', [])
        budget = data.get('budget')
        relation = data.get('relation')

        if not all([gender, age_group, budget, relation]):
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # تگ‌های غیر interest (برای همه درخواست‌ها مشترک هستند)
        base_tag_values = {
            "gender": gender,
            "age_group": age_group,
            "budget": budget,
            "relation": relation,
        }

        # گرفتن تگ‌های ثابت (غیر از interest)
        base_tags = Tag.objects.filter(
            Q(category="gender", value=gender) |
            Q(category="age_group", value=age_group) |
            Q(category="budget", value=budget) |
            Q(category="relation", value=relation)
        )
        base_tag_ids = set(tag.id for tag in base_tags)

        matched_suggestions = set()

        # برای هر interest یک بار جدا بررسی می‌کنیم
        for interest in interests:
            interest_tag = Tag.objects.filter(category="interest", value=interest).first()
            if not interest_tag:
                continue  # interest نامعتبر

            current_tag_ids = base_tag_ids.union({interest_tag.id})

            # بررسی تمام پیشنهادها
            for suggestion in GiftSuggestion.objects.prefetch_related('tags').all():
                suggestion_tags = suggestion.tags.all()

                # دسته‌بندی تگ‌ها بر اساس کتگوری
                tags_by_category = {}
                for tag in suggestion_tags:
                    tags_by_category.setdefault(tag.category, []).append(tag.value)

                match = True
                for category, selected_value in base_tag_values.items():
                    if category in tags_by_category:
                        if selected_value not in tags_by_category[category]:
                            match = False
                            break
                    # اگر در این دسته تگی وجود نداشت، یعنی با همه سازگاره → قبول

                # بررسی interest
                if "interest" in tags_by_category:
                    if interest not in tags_by_category["interest"]:
                        match = False

                if match:
                    matched_suggestions.add(suggestion)

        # مرتب‌سازی و برگشت ۱۰ مورد برتر
        sorted_suggestions = sorted(matched_suggestions, key=lambda s: s.score, reverse=True)[:10]
        serializer = GiftSuggestionSerializer(sorted_suggestions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
class RegisterClickAPI(APIView):
    def post(self, request):
        print('scored')
        suggestion_id = request.data.get("suggestion_id")
        if not suggestion_id:
            return Response({"error": "Missing suggestion_id"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            suggestion = GiftSuggestion.objects.get(id=suggestion_id)
            suggestion.score += 1
            suggestion.save()
            return Response({"success": True, "new_score": suggestion.score}, status=status.HTTP_200_OK)
        except GiftSuggestion.DoesNotExist:
            return Response({"error": "Suggestion not found"}, status=status.HTTP_404_NOT_FOUND)
