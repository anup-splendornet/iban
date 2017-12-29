from django import forms
from django.contrib.auth.models import User
from .models import IbanInfo
from schwifty import IBAN

class IbanInfoForm(forms.ModelForm):    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(IbanInfoForm, self).__init__(*args, **kwargs)    

    def clean(self):        
        cleaned_data = super(IbanInfoForm, self).clean()
        try:
            ibanvalue = IBAN(cleaned_data.get('iban'))
        except Exception as msg:
            self.add_error('iban', msg)

    class Meta:
        model = IbanInfo
        fields = ('first_name', 'last_name', 'iban')
        widgets={            
            'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter First Name'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Last Name'}),
            'iban' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter IBAN Number'}),            
        }
        error_messages={            
            'first_name':{
                'required':'Please Enter First Name.'
            },
            'last_name':{
                'required':'Please Enter Last Name.'
            },
            'iban': {
                'required': 'Please Enter IBAN Number.'
            }                      
        }    