from django.test import TestCase
from .models import IbanDetails
from django.db.utils import IntegrityError
from django.core.management import call_command
from .forms import IbanDetailsForm
# Create your tests here.
class IbanModelTestCase(TestCase):

    def setUp(self):
        fixtures = 'group_admin.json'
        call_command('loaddata', fixtures, verbosity=0)

    def test_iban_details_model(self):
        """
        Model specific unittest.
        Should check create object of IbanDetails.
        """
        detail = IbanDetails.objects.create(first_name = "anup",
            last_name = "yadav",iban_number = "123456789012",status = True,
            creator_id = "1",created_at = "2017-12-29 12:33:52.94701+05:30",
            updated_at = "2017-12-29 12:33:52.94701+05:30")
        self.assertIsInstance(detail,IbanDetails)

    def test_str_is_equal_to_iban_number(self):
        """
        Model specific unittest.
        Method `__str__` should be equal to field `title`
        """
        iban = IbanDetails.objects.get(pk=1)
        self.assertEqual(str(iban), iban.iban_number)

class IbanFormTestCase(TestCase):
    
    def setUp(self):
        pass

    def test_form_success(self):
        """
            To check Form is valid or not.
        """
        form_data = {
            "first_name":"anup",
            "last_name":"yadav",
            "iban_number":"DE89 3704 0044 0532 0130 00",
        }
        form = IbanDetailsForm(data=form_data)
        self.assertTrue(form.is_valid())

    #Iban number exception.
    def test_form_error(self):
        """
            To check Form is testing to perfect Iban number or not.
        """
        form_data = {
            "first_name":"anup",
            "last_name":"yadav",
            "iban_number":"123456789",
        }
        form = IbanDetailsForm(data=form_data)
        #for error in form.errors:print(error) This should raise exception to IBAN number.
        self.assertFalse(form.is_valid())