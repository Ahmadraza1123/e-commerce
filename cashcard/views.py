from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import CashCard
from .serializers import CashCardSerializer

class CashCardViewSet(viewsets.ModelViewSet):
    queryset = CashCard.objects.all()
    serializer_class = CashCardSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        return CashCard.objects.filter(user=self.request.user)

    def perform_create(self, serializer):

        if CashCard.objects.filter(user=self.request.user).exists():
            raise ValidationError({"detail": "You already have a cash card."})
        serializer.save(user=self.request.user)
