"""
URL configuration for referal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import (UserRegistrationAPIView, ReferralCodeAPIView,
                       GetReferralCodeByEmailView, DeleteReferralCodeView,
                       GetReferralsView, GetReferralByUserView, RegisterUserByReferralView)

urlpatterns = [

    path('admin/', admin.site.urls),

    # Регистрация пользователя
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),

    # Работа с реферальными кодами
    path('referral-code/', ReferralCodeAPIView.as_view(), name='referral-code'),
    path('get-referral-code-by-email/', GetReferralCodeByEmailView.as_view(), name='get-referral-code-by-email'),
    path('delete-referral-code/<int:id>/', DeleteReferralCodeView.as_view(), name='delete-referral-code'),

    # Работа с рефералами
    # path('referral/', ReferralAPIView.as_view(), name='referral'),
    path('get-referrals/', GetReferralsView.as_view(), name='get-referrals'),
    path('get-referral-by-user/<int:id>/', GetReferralByUserView.as_view(), name='get-referral-by-user'),

    # Регистрация по реферальному коду
    path('register-by-referral-code/', RegisterUserByReferralView.as_view(), name='register-by-referral-code'),
]
