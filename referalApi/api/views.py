from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ReferralCode, Referral
from .serializers import UserSerializer, ReferralCodeSerializer, ReferralSerializer
from datetime import datetime


User = get_user_model()

class UserRegistrationAPIView(APIView):
    """Регистрация нового пользователя"""
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReferralCodeAPIView(APIView):
    """Создание и удаление реферального кода"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Получение реферального кода пользователя"""
        try:
            referral_code = ReferralCode.objects.get(user=request.user)
            serializer = ReferralCodeSerializer(referral_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ReferralCode.DoesNotExist:
            return Response({"detail": "Реферальный код не существует."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """Создание нового реферального кода"""
        try:
            # Проверка, есть ли уже активный код
            existing_code = ReferralCode.objects.get(user=request.user)
            return Response({"detail": "У вас уже есть активный реферальный код."}, status=status.HTTP_400_BAD_REQUEST)
        except ReferralCode.DoesNotExist:
            # Создание нового реферального кода
            expires_at = request.data.get("expires_at")
            if not expires_at:
                return Response({"detail": "Необходимо указать срок годности кода."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                expires_at = datetime.fromisoformat(expires_at)
            except ValueError:
                return Response({"detail": "Неверный формат даты."}, status=status.HTTP_400_BAD_REQUEST)

            # Проверка, не существует ли уже активного кода с таким сроком годности
            existing_code_with_expires_at = ReferralCode.objects.filter(user=request.user, expires_at=expires_at)
            if existing_code_with_expires_at.exists():
                return Response({"detail": "У вас уже есть действующий реферальный код с таким сроком годности."}, status=status.HTTP_400_BAD_REQUEST)

            referral_code = ReferralCode.objects.create(user=request.user, expires_at=expires_at)
            serializer = ReferralCodeSerializer(referral_code)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        """Удаление реферального кода"""
        try:
            referral_code = ReferralCode.objects.get(user=request.user)
            referral_code.delete()
            return Response({"detail": "Реферальный код удален."}, status=status.HTTP_204_NO_CONTENT)
        except ReferralCode.DoesNotExist:
            return Response({"detail": "Реферальный код не существует."}, status=status.HTTP_404_NOT_FOUND)


class GetReferralCodeByEmailView(APIView):
    """Получение реферального кода по email адресу реферера"""
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        referral_code = ReferralCode.objects.get(user=request.user)
        serializer = ReferralCodeSerializer(referral_code)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterUserByReferralView(APIView):
    """Регистрация пользователя по реферальному коду"""
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        referred_by = request.data.get("referral_code")
        if not referred_by:
            return Response({"detail": "Необходимо указать реферальный код."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            referrer = User.objects.get(referral_code__code=referred_by)
        except User.DoesNotExist:
            return Response({"detail": "Неверный реферальный код."}, status=status.HTTP_400_BAD_REQUEST)

        # Создание связи между реферером и рефералом
        if Referral.objects.filter(referred=request.user).exists():
            return Response({"detail": "Этот пользователь уже зарегистрирован по реферальному коду."}, status=status.HTTP_400_BAD_REQUEST)

        Referral.objects.create(refer=referrer, referred=request.user)
        return Response({"detail": "Вы успешно зарегистрированы по реферальному коду."}, status=status.HTTP_201_CREATED)


class GetReferralsView(APIView):
    """Получение рефералов для текущего пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        referrals = Referral.objects.filter(refer=request.user)
        serializer = ReferralSerializer(referrals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteReferralCodeView(APIView):
    """Удаление реферального кода"""
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        referral_code_id = kwargs.get("id")
        if not referral_code_id:
            return Response({"detail": "Необходимо указать ID реферального кода."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            referral_code = ReferralCode.objects.get(id=referral_code_id)
            referral_code.delete()
            return Response({"detail": "Реферальный код удален."}, status=status.HTTP_204_NO_CONTENT)
        except ReferralCode.DoesNotExist:
            return Response({"detail": "Реферальный код не существует."}, status=status.HTTP_404_NOT_FOUND)


class GetReferralByUserView(APIView):
    """Получение реферала для текущего пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        referral_code_id = kwargs.get("id")
        if not referral_code_id:
            return Response({"detail": "Необходимо указать ID реферального кода."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            referral_code = ReferralCode.objects.get(id=referral_code_id)
            serializer = ReferralCodeSerializer(referral_code)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ReferralCode.DoesNotExist:
            return Response({"detail": "Реферальный код не существует."}, status=status.HTTP_404_NOT_FOUND)