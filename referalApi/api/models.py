import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


def generate_referral_code():
    return str(uuid.uuid4())[:10]


class User(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_groups",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions",
        blank=True,
    )


class ReferralCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referral_code')
    code = models.CharField(max_length=10, unique=True, default=generate_referral_code())
    expires_at = models.DateTimeField(auto_now_add=True)


class Referral(models.Model):
    refer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_users')
    referred = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referred_by')
    created_at = models.DateTimeField(auto_now_add=True)

