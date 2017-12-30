from django.test import TestCase
from django.contrib.auth.models import User, Group
from ibanmanagment.models import IbanDetails
from django.core.management import call_command
from django.core.urlresolvers import reverse

# Create your tests here.
class IbanCreateUpdateDeleteViewTestCase(TestCase):
    
    def iban_create_update_delete_test_permission(self):
        """
        Iban create and update view.
        Should not reach to the page of create and update of IbanDetails, should display error of permission denied.
        """
        #Create View UnitTest
        user = User.objects.create_user(username='flyuser',email='flyuser@gmail.com',password='flyuser')
        login = self.client.login(username='flyuser', password='flyuser')
        response = self.client.get(reverse('createiban'))
        self.assertTrue('Permission Denied - Error 403' in str(response.content))

        #Update View UnitTest
        url = reverse('updateiban', args=[1])
        self.assertEqual(url, '/updateiban/1/')
        response = self.client.get(url)
        self.assertTrue('Permission Denied - Error 403' in str(response.content))

    def iban_create_update_delete_test_valid(self):
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
        #Checking for Valid IBAN message.
        self.assertTrue('This Iban is not valid. Please correct and try again.' in str(response.content))
        ibanformdata['iban_number'] = "EE38 2200 2210 2014 5685"
        response = self.client.post("/createiban/", ibanformdata)
        iban = IbanDetails.objects.last()
        #Checking for perfect insertion.
        self.assertEqual(iban.iban_number, "EE38 2200 2210 2014 5685")
        response = self.client.post("/createiban/", ibanformdata)
        #Should not allow duplicate IBAN, this won't but still added in unittest for future reference. 
        self.assertTrue('Iban Details with this Iban number already exists.' in str(response.content))

        self.client.logout()
        dummyuser = User.objects.create_user(username='dummyuser',email='dummyuser@gmail.com',password='dummyuser')
        #Login through hacking user / administrator, and trying to access update page of another Iban creator.
        login = self.client.login(username='dummyuser', password='dummyuser')
        url = reverse('updateiban', args=[1])
        self.assertEqual(url, '/updateiban/1/')
        response = self.client.get(url)
        #Expected output is Permission Denied.
        self.assertTrue('Permission Denied - Error 403' in str(response.content))

        #Now trying to post values using dummy user, so changing creator and it must return Permission debied error.
        #Ownership permission has to be tested in post as well.
        response = self.client.post(url, ibanformdata)        
        ibanformdata['creator'] = dummyuser.id
        response = self.client.post(url, ibanformdata)
        #Expected output is Permission Denied.
        self.assertTrue('Permission Denied - Error 403.' in str(response.content))



