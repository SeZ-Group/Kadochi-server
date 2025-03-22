from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import random
import json

from suggestions.models import GiftSuggestion


# VIEWS
@method_decorator(csrf_exempt, name='dispatch')
class SuggestionAPI(View):
    def post(self, request):
        try:
            print('got api')
            data = json.loads(request.body)
            gender = data.get('gender')
            relation = data.get('relation')
            age_group = data.get('age_group')
            interest = data.get('interest')
            budget = data.get('budget')

            suggestions = GiftSuggestion.objects.filter(
                gender=gender,
                relation=relation,
                age_group=age_group,
                interest=interest,
                budget=budget
            )

            results = random.sample(list(suggestions), min(5, suggestions.count()))
            return JsonResponse([s.as_dict() for s in results], safe=False)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

