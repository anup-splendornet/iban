from django.contrib import admin
from .models import IbanInfo
from .forms import IbanInfoForm

# Register your models here.
class IbanInfoAdmin(admin.ModelAdmin):
    fields = (('first_name', 'last_name'), ('iban', 'owner'))
    form  = IbanInfoForm
    list_display = ('first_name', 'last_name', 'iban')
    search_fields =('first_name', 'last_name', 'iban')
admin.site.register(IbanInfo, IbanInfoAdmin)
