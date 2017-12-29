from django import forms
from django.forms import widgets
from ibanmanage import models
from django.db.models import Q
from schwifty import IBAN
from django.core.validators import RegexValidator

regex_validator = RegexValidator(r"^([a-zA-Z'\u00c0-\u017e]+)$", "Please enter a valid value.")

class IbandataCreateForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super (IbandataCreateForm,self ).__init__(*args,**kwargs)
        self.fields['first_name'].validators = [regex_validator]
        self.fields['last_name'].validators = [regex_validator]
    def clean(self):
        cleaned_data = super(IbandataCreateForm, self).clean()
        try:
            ibanvalue = IBAN(cleaned_data.get('iban'))
        except Exception as msg:
            self.add_error('iban',msg)
        # avoid duplicate iabn
        duplicate_iban = models.Ibandata.objects.filter(Q(iban__exact = cleaned_data.get('iban'))).count()
        if duplicate_iban > 0:
                self.add_error('iban',"%s already exist in database." % cleaned_data.get('iban'))
        return self.cleaned_data
    class Meta:
        model = models.Ibandata
        fields = ['first_name','last_name','iban']
        widgets = {
            'first_name':widgets.TextInput(attrs={'class':'form-control'}),
            'last_name':widgets.TextInput(attrs={'class':'form-control'}),
            'iban':widgets.TextInput(attrs={'class':'form-control'}),
        }
        error_messages = {
            'first_name':{
                'required':'Please Enter First Name.'
            },
            'last_name':{
                'required':'Please Enter Last Name.'
            },
            'iban':{
                'required':'Please Enter IBAN.'
            }
        }