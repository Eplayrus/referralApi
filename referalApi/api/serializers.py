from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import ReferralCode, Referral

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ReferralCodeSerializer(serializers.ModelSerializer):
    """Сериализатор для реферального кода"""
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReferralCode
        fields = ['user', 'code', 'expires_at']


class ReferralSerializer(serializers.ModelSerializer):
    """Сериализатор для рефералов"""
    refer = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    referred = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Referral
        fields = ['id', 'refer', 'referred', 'created_at']

    def validate(self, data):
        """Проверяем, что пользователь не может быть рефералом у нескольких пользователей"""
        if Referral.objects.filter(referred=data['referred']).exists():
            raise serializers.ValidationError("Этот пользователь уже зарегистрирован по реферальному коду.")
        return data
