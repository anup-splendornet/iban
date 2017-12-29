from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

# changing the behaviour of email attribute of User model, making it unique
User._meta.get_field('email')._unique = True

class IbanInfo(models.Model):
    first_name = models.CharField(max_length=100, blank=False, null=False, verbose_name="First Name")
    last_name = models.CharField(max_length=100, blank=False, null=False, verbose_name="Last Name")
    iban = models.CharField(max_length=100, blank=False, null=False, unique=True, verbose_name="IBAN Number")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_admin')

    class Meta:
        db_table = 'iban_info'
        verbose_name ='IBAN Information'
        verbose_name_plural ='IBAN Informations'
    
    def __str__(self):
        return self.first_name+' '+self.last_name
