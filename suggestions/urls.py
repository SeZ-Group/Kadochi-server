from django.urls import path
from .views import SuggestionAPI

urlpatterns = [
    path('api/suggestions/', SuggestionAPI.as_view(), name='suggestions'),
]
