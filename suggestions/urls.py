from django.urls import path
from .views import SuggestionAPI, RegisterClickAPI

urlpatterns = [
    path('suggest/', SuggestionAPI.as_view(), name='suggestions'),
    path('click/', RegisterClickAPI.as_view(), name='register-click'),
]
