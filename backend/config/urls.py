from django.contrib import admin
from django.urls import path, include, re_path
from .views import IndexView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/votes/', include('apps.votes.urls')),
    re_path('', IndexView.as_view()),
]
