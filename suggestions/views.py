from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import random
import json

from suggestions.models import GiftCondition, GiftSuggestion

@method_decorator(csrf_exempt, name='dispatch')
class SuggestionAPI(View):
    def post(self, request):
        try:
            print('got api')
            data = json.loads(request.body)

            gender = data.get('gender')
            relation = data.get('relation')
            age_group = data.get('age_group')
            interests = data.get('interests', [])
            budget = data.get('budget')

            try:
                condition = GiftCondition.objects.get(
                    gender=gender,
                    relation=relation,
                    age_group=age_group,
                    interests=interests,
                    budget=budget
                )
            except GiftCondition.DoesNotExist:
                return JsonResponse([], safe=False)

            suggestions = condition.suggestions.all().order_by('-score') 
            selected = random.sample(list(suggestions), min(5, suggestions.count()))

            return JsonResponse([s.as_dict() for s in selected], safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
