from django.db import models
from user.models import User
from utils.constraints import LENGTH


class Contact(models.Model):
    name = models.CharField(max_length=LENGTH.NAME, blank=False, null=False)
    phone_number = models.CharField(max_length=LENGTH.PHONE_NUMBER, blank=False, null=False)
    email = models.EmailField(max_length=LENGTH.EMAIL, blank=True, null=True)
    objects = models.Manager()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name
    
class Spam(models.Model):
    
    phone_number = models.CharField(max_length=LENGTH.PHONE_NUMBER, null=False, blank=False)
    marked_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    class Meta:
        unique_together = ('phone_number', 'marked_by')