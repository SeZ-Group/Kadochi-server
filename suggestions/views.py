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

class SuggestionAPI(APIView):
    def post(self, request):
        data = request.data
        print('api called')

        gender = data.get('gender')
        age_group = data.get('age_group')
        interests = data.get('interest', [])
        budget = data.get('budget')

        all_suggestions = []

        for interest in interests:
            try:
                condition = GiftCondition.objects.get(
                    gender=gender,
                    age_group=age_group,
                    interest=interest,
                    budget=budget
                )
                suggestions = list(condition.suggestions.all())
                all_suggestions.extend(suggestions)
            except GiftCondition.DoesNotExist:
                continue 

        unique_suggestions = {s.id: s for s in all_suggestions}.values()

        sorted_suggestions = sorted(unique_suggestions, key=lambda s: s.score, reverse=True)[:10]

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
