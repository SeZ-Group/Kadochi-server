from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from suggestions.models import GiftCondition
from .serializers import GiftSuggestionSerializer
import random

class SuggestionAPI(APIView):
    def post(self, request):
        print('api called')
        data = request.data

        gender = data.get('gender')
        relation = data.get('relation')
        age_group = data.get('age_group')
        interest = data.get('interest')
        budget = data.get('budget')

        try:
            condition = GiftCondition.objects.get(
                gender=gender,
                relation=relation,
                age_group=age_group,
                interest=interest,
                budget=budget
            )
        except GiftCondition.DoesNotExist:
            return Response([], status=status.HTTP_200_OK)

        suggestions = condition.suggestions.all().order_by('-score')
        selected = random.sample(list(suggestions), min(5, suggestions.count()))
        serializer = GiftSuggestionSerializer(selected, many=True)

        return Response(serializer.data)
