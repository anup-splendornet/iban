from django.contrib import admin
from ibanmanage.models import Ibandata
from ibanmanage import forms


# Register your models here.
@admin.register(Ibandata)
class IbandataAdmin(admin.ModelAdmin):
    form = forms.IbandataCreateForm
    fields = (('first_name','last_name'),('iban','created_by'))
    list_display = ('first_name','last_name','iban','created_by')
    search_fields = ('first_name','last_name','iban','created_by')

