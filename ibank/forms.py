from django import forms
from .models import BankUser

class clientUserDetailForm(forms.Form):
    first_name=forms.CharField(label="First Name")
    last_name=forms.CharField(label="Last Name")
    bank_no=forms.CharField(label="Bank No")
    class Meta:
        model=BankUser
        fields=['first_name','last_name','bank_no']
        widgets={
            'first_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter First Name'}),
            'last_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Last Name'}),
            'bank_no' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Bank No'}),
        }