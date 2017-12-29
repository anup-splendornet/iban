from django.test import TestCase
from django.contrib.auth.models import User
from .models import Ibandata
from ibanmanage import forms

# Create your tests here.
class IbandataModelTest(TestCase):
    def setUp(self):
        self.username = 'firstuser'
        self.password = 'firstuserpwd'
        self.user = User.objects.create_user(username=self.username, password=self.password, email='test1@yopmail.com', is_active=True)

    def test_string_representation(self):
        fname = "fname"
        lname = "lname"
        iban = "ABC123"
        ibanUser = Ibandata(first_name=fname, last_name=lname, iban=iban,created_by=self.user)
        self.assertEqual(str(fname), ibanUser.first_name)

    def test_user_instance(self):
        fname = "fname"
        lname = "lname"
        iban = "ABC123"
        ibanUser = Ibandata(first_name=fname, last_name=lname, iban=iban,created_by=self.user)
        self.assertIs(type(ibanUser.created_by), User)


class IbanFormTestCase(TestCase):

    def setUp(self):
        self.username = 'firstuser'
        self.password = 'firstuserpwd'
        self.user = User.objects.create_user(username=self.username, password=self.password, email='test1@yopmail.com', is_active=True)

    def test_form_working(self):
        form_data = {
            "first_name":"fname",
            "last_name":"lname",
            "iban":"HR12 1001 0051 8630 0016 0",
        }
        form = forms.IbandataCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_error(self):
        form_data = {
            "first_name":"fname",
            "last_name":"lname",
            "iban":"AB12 345",
        }
        form = forms.IbandataCreateForm(data=form_data)
        self.assertFalse(form.is_valid())