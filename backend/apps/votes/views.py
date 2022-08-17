from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import VoteSerializer
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class VoteCreateAPIView(CreateAPIView):
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if self.is_reserve(serializer.validated_data['start_datetime']):
            status = 0
        else:
            status = 1
        serializer.save(status=status, author=user)

    def is_reserve(self, start_datetime):
        if (timezone.now() < start_datetime):
            return True
        else:
            return False
