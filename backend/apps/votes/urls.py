from django.urls import path, include
from .views import VoteCreateAPIView

urlpatterns = [
    path('create/', VoteCreateAPIView.as_view()),
]
