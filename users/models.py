from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        OPERATOR = 'OPERATOR', 'Operator'
        SELLER = 'SELLER', 'Seller'
        CUSTOMER = 'CUSTOMER', 'Customer'
        COURIER = 'COURIER', 'Courier'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        PENDING_VERIFICATION = 'PENDING_VERIFICATION', 'Pending Verification'
        SUSPENDED = 'SUSPENDED', 'Suspended'
        BLOCKED = 'BLOCKED', 'Blocked'
        DELETED = 'DELETED', 'Deleted'

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.ACTIVE)

    def __str__(self):
        return f'{self.user.username} ({self.role})'
