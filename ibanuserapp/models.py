from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
User._meta.get_field('email')._unique = True

class IbanUserInfo(models.Model):
    #define fields
    first_name=models.CharField(max_length=80)
    last_name=models.CharField(max_length=80)
    iban_num=models.CharField(max_length=100,unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='iban_admin')
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        #ordered as last inserted record first
        ordering=["-created_at"]

        db_table = 'iban_user_info'
        verbose_name ='IBAN User Information'
        verbose_name_plural ='IBAN Users Information'

    def __str__(self):
        #return unique iban string
        return self.iban_num