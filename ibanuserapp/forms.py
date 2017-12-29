from django import forms
from .models import IbanUserInfo

class IbanUserInfoForm(forms.Form):
    first_name=forms.CharField(label="First Name")
    last_name=forms.CharField(label="Last Name")
    iban_num=forms.CharField(label="IBAN")
    class Meta:
        model=IbanUserInfo
        fields=['first_name','last_name','iban_num']
        widgets={            
            'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter First Name'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Last Name'}),
            'iban_num' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter IBAN'}),            
        }