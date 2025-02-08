from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AsyncReferralCodeViewSet, AsyncReferralViewSet

router = DefaultRouter()
router.register(r'referral_codes', AsyncReferralCodeViewSet)
router.register(r'referrals', AsyncReferralViewSet)

urlpatterns = [
    path('', include(router.urls)),
]