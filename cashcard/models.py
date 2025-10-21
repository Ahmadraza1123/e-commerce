from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class CashCard(models.Model):
    card_number = models.CharField(max_length=11, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cashcard")
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Balance: {self.amount}"
