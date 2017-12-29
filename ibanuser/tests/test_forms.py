from django.test import TestCase
from django.contrib.auth.models import User
from ibanuser.forms import IbanInfoForm

class IBanInfoFormTestCase(TestCase):
    def setUp(self):
        self.username = 'myuser'
        self.password = 'valid_password1'         
        self.user = User.objects.create_user(username=self.username, email='email@test.com', is_active=True, password=self.password)

    def test_ibanuserform_valid(self):        
        form = IbanInfoForm(data={'first_name': "first", 'last_name': "last", 'iban': "AT61 1904 3002 3457 3201", 'owner': self.user.id})
        self.assertTrue(form.is_valid())

    def test_ibanuserform_invalid(self):
        form = IbanInfoForm(data={'first_name': "", 'last_name': "last", 'iban': "RTSEFG3434", 'owner': self.user.id})  
        self.assertFalse(form.is_valid())
