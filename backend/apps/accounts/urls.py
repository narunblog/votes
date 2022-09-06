from django.urls import path, include
from .views import celery_test


urlpatterns = [
    path('celery_test/', celery_test, name='celery_test'),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]
