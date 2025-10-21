from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import CashCard

User = get_user_model()

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'role', 'address', 'user_profile']

class CashCardSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer(read_only=True)

    class Meta:
        model = CashCard
        fields = ['id', 'card_number','amount', 'user']
