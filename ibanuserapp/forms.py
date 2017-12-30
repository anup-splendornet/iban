from django import forms
from .models import IbanUserInfo
from schwifty import IBAN

class IbanUserInfoForm(forms.ModelForm):
    first_name=forms.CharField(label="First Name")
    last_name=forms.CharField(label="Last Name")
    iban_num=forms.CharField(label="IBAN")

    def __init__(self, *args, **kwargs):
        super(IbanUserInfoForm, self).__init__(*args, **kwargs)

    def clean(self):        
        cleaned_data = super(IbanUserInfoForm, self).clean()
        try:
            ibanvalue = IBAN(cleaned_data.get('iban_num'))
        except Exception as msg:
            self.add_error('iban_num', msg)

    class Meta:
        model=IbanUserInfo
        fields=['first_name','last_name','iban_num']
        widgets={            
            'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter First Name'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Last Name'}),
            'iban_num' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter IBAN'}),            
        }
        error_messages={
            'first_name': {
                'required': 'Please enter the first name.'
            },
            'last_name': {
                'required': 'Please enter the last name.'
            },
            'iban_num': {
                'required': 'Please enter the iban number.'
            }
        }