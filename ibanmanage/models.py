from django.db import models
from django.contrib.auth.models import User

class TimestampOwnerMixin(models.Model):
    date_created = models.DateTimeField(null=True,auto_now_add=True)
    date_modified = models.DateTimeField(null=True,auto_now=True)
    class Meta:
        abstract = True

class Ibandata(TimestampOwnerMixin, models.Model):
    first_name = models.CharField(max_length=30, null=False, blank=False, verbose_name="First Name")
    last_name = models.CharField(max_length=30, null=False, blank=False, verbose_name="Last Name")
    iban = models.CharField(max_length=128, null=False, unique=True, blank=False, verbose_name="IBAN")
    created_by = models.ForeignKey(User, models.DO_NOTHING, related_name="parent",blank=False, null=False,default=1)

    class Meta:
        db_table = 'iban_data'

    def __str__(self):
        return self.first_name

User._meta.get_field('email')._unique = True

