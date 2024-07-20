from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.constraints import LENGTH
from django.contrib.auth.models import Group, Permission

# Model for User
class User(AbstractUser):
    name = models.CharField(max_length=LENGTH.NAME, blank=False, null=False, unique=False)
    email = models.EmailField(max_length=LENGTH.EMAIL, blank=True, null=True, unique=False)
    country = models.CharField(max_length=5, blank=True, null=True, unique=False)
    joined_date = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(
        max_length=LENGTH.PHONE_NUMBER,
        unique=True,
        error_messages={
            'unique': "A user with that phone number already exists.",
        }
    )
    groups = models.ManyToManyField(
        Group,
        related_name='user_groups',
        blank=True,
        help_text='Groups the user belongs to. Grants all permissions of these groups.',
        verbose_name=('groups'),
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='user_permissions', 
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name=('user permissions'),
    )
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.phone_number