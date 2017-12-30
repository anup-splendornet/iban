from django.test import TestCase
from django.contrib.auth.models import User, Group
from ibanmanagment.models import IbanDetails
from django.core.management import call_command
from django.core.urlresolvers import reverse

# Create your tests here.
class IbanCreateViewTestCase(TestCase):
    
    def iban_create_test_permission(self):
        """
        Iban create view.
        Should not create objects of IbanDetails, should display error of permission denied.
        """
        user = User.objects.create_user(username='flyuser',email='flyuser@gmail.com',password='flyuser')
        login = self.client.login(username='flyuser', password='flyuser')
        response = self.client.get(reverse('createiban'))
        #self.assertEqual(response.status_code, 403)
        self.assertTrue('Permission Denied - Error 403' in response.content)

    def iban_create_test_valid(self):
        """
        Iban create view.
        Should be create objects of IbanDetails.
        """
        fixtures = 'permission_group.json'
        call_command('loaddata', fixtures, verbosity=0)
        user = User.objects.create_user(username='flyuser',email='flyuser@gmail.com',password='flyuser')
        group = Group.objects.get(pk=1)
        user.groups.add(group)
        login = self.client.login(username='flyuser', password='flyuser')
        response = self.client.get(reverse('createiban'))
        self.assertEqual(response.status_code, 200)
        ibanformdata = {
            "first_name":"anup",
            "last_name":"yadav",
            "iban_number":"123456789",
            "status":True,
            "creator":user.id,
            "created_at":"2017-12-26 12:33:52.94701+05:30",
            "updated_at":"2017-12-26 12:33:52.94701+05:30"
        }
        response = self.client.post("/createiban/", ibanformdata)
        self.assertTrue('This Iban is not valid. Please correct and try again.' in str(response.content))
        ibanformdata['iban_number'] = "EE38 2200 2210 2014 5685"
        response = self.client.post("/createiban/", ibanformdata)
        iban = IbanDetails.objects.last()
        self.assertEqual(iban.iban_number, "EE38 2200 2210 2014 5685")
        response = self.client.post("/createiban/", ibanformdata)
        self.assertTrue('Iban Details with this Iban number already exists.' in str(response.content))


