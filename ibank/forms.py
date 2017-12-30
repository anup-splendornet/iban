from django import forms
from .models import BankUser
from schwifty import IBAN

class ClientUserDetailForm(forms.ModelForm):
    first_name=forms.CharField(label="First Name")
    last_name=forms.CharField(label="Last Name")
    bank_no=forms.CharField(label="Bank No")
    class Meta:
        model=BankUser
        fields=('first_name','last_name','bank_no')
        widgets={
            'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter First Name'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Last Name'}),
            'bank_no' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Bank No'}),
        }
    def clean(self):
        cleaned_data = super(ClientUserDetailForm, self).clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        bank_no = cleaned_data.get('bank_no')
        if not first_name and not last_name and not bank_no:
            raise forms.ValidationError('All Fields Are Required')
        try:
            ibanvalue = IBAN(cleaned_data.get('bank_no'))
        except Exception as msg:
            self.add_error('bank_no', msg)