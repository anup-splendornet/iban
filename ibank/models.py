from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BankUser(models.Model):
    bank_no = models.CharField(max_length = 100, null=False, blank=False, unique=True, verbose_name="Bank No")
    first_name = models.CharField(max_length = 30, null=False, blank=False, verbose_name="First Name")
    last_name = models.CharField(max_length = 30, null=False, blank=False, verbose_name="Last Name")
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name="user_created_by")