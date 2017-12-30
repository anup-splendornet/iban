from django.test import TestCase
from django.contrib.auth.models import User, Group, Permission
from .models import Ibandata
from ibanmanage import forms
from django.core.management import call_command
from django.core.urlresolvers import reverse



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

class IbanListViewTestCase(TestCase):

    def setUp(self):
        self.username = 'firstuser'
        self.password = 'firstuserpwd'
        self.user = User.objects.create_user(username=self.username, password=self.password, email='test1@yopmail.com', is_active=True)

    #Un-authenticated users should be redirected
    def test_listview_unauth_user(self):
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, '/login/?next=/dashboard/')
        self.assertEqual(response.status_code, 302)

    #Dashboard should work for logged in user.
    def test_dashboard_list(self):

        ibanUser1 = Ibandata.objects.create(first_name='fname', last_name='lname', iban='AL47 2121 1009 0000 0002 3569 8741',created_by=self.user)
        ibanUser2 = Ibandata.objects.create(first_name='fname', last_name='lname', iban='AD12 0001 2030 2003 5910 0100',created_by=self.user)
        ibanUser3 = Ibandata.objects.create(first_name='fname', last_name='lname', iban='AT61 1904 3002 3457 3201',created_by=self.user)

        login = self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context.get('ibandata_list')),2)

    def test_dashboard_blank_list(self):
        user = User.objects.create_user(username='seconduser',email='seconduser@yopmail.com',password='seconduserpwd')
        login = self.client.login(username='seconduser', password='seconduserpwd')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"No Data")


class IbanCreateViewTestCase(TestCase):

    def setUp(self):
        self.username = 'firstuser'
        self.password = 'firstuserpwd'
        self.user = User.objects.create_user(username=self.username, password=self.password, email='test1@yopmail.com', is_active=True)

    def test_created_iban_user(self):
        
        all_permissions = Permission.objects.filter(content_type__app_label='ibanmanage', content_type__model='ibandata')
        #create group
        group = Group.objects.create(name='Ibanadmin')
        # assign permissions
        for permission in all_permissions:
            group.permissions.add(permission)

        self.user.groups.add(group)

        login = self.client.login(username=self.username, password=self.password)
        firstuser = self.client.post('/addibandata/', {'first_name':"fname", 'last_name': "lname", 'iban':"AL47 2121 1009 0000 0002 3569 8741","created_by":self.user})
        seconduser = self.client.post('/addibandata/', {'first_name':"fname", 'last_name': "lname", 'iban':"AL47 2121 1009 0000 0002 3569 8741","created_by":self.user})

        self.assertEqual(seconduser.status_code, 200)
        self.assertContains(seconduser,"already exist in database")

class IbanUpdateViewTestCase(TestCase):

    def setUp(self):
        self.username = 'firstuser'
        self.password = 'firstuserpwd'
        self.user = User.objects.create_user(username=self.username, password=self.password, email='test1@yopmail.com', is_active=True)

        self.username2 = 'seconduser'
        self.password2 = 'seconduserpwd'
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2, email='test2@yopmail.com', is_active=True)


    def test_update_iban_user(self):

        all_permissions = Permission.objects.filter(content_type__app_label='ibanmanage', content_type__model='ibandata')
        #create group
        group = Group.objects.create(name='Ibanadmin')
        # assign permissions
        for permission in all_permissions:
            group.permissions.add(permission)

        self.user.groups.add(group)

        login = self.client.login(username=self.username, password=self.password)
        firstuser = self.client.post('/addibandata/', {'first_name':"fname", 'last_name': "lname", 'iban':"AL47 2121 1009 0000 0002 3569 8741","created_by":self.user})
        seconduser = self.client.post('/addibandata/', {'first_name':"fname", 'last_name': "lname", 'iban':"GR16 0110 1250 0000 0001 2300 695","created_by":self.user})
        latest_id = Ibandata.objects.latest('id')
        updateseconduser = self.client.post('/editibandata/'+str(latest_id.id)+'/', {'first_name':"fname", 'last_name': "lname", 'iban':"AL47 2121 1009 0000 0002 3569 8741","created_by":self.user})

        self.assertContains(updateseconduser,"already exist in database")


    def test_update_iban_ownership(self):
        all_permissions = Permission.objects.filter(content_type__app_label='ibanmanage', content_type__model='ibandata')
        #create group
        group = Group.objects.create(name='Ibanadmin')
        # assign permissions
        for permission in all_permissions:
            group.permissions.add(permission)

        self.user.groups.add(group)
        self.user2.groups.add(group)

        ibanUser1 = Ibandata.objects.create(first_name='fname', last_name='lname', iban='AL47 2121 1009 0000 0002 3569 8741',created_by=self.user)
        ibanUser2 = Ibandata.objects.create(first_name='fname', last_name='lname', iban='AD12 0001 2030 2003 5910 0100',created_by=self.user)
        ibanUser3 = Ibandata.objects.create(first_name='fname', last_name='lname', iban='AT61 1904 3002 3457 3201',created_by=self.user2)

        login = self.client.login(username=self.username2, password=self.password2)

        updateseconduser = self.client.get('/editibandata/2/')
        self.assertContains(updateseconduser,"Forbidden - Error 403")

        updateseconduser2 = self.client.post('/editibandata/2/', {'first_name':"fname", 'last_name': "lname", 'iban':"EE38 2200 2210 2014 5685","created_by":self.user2})
        self.assertContains(updateseconduser2,"Forbidden - Error 403")


class IbanDeleteViewTestCase(TestCase):

    def setUp(self):
        self.username = 'firstuser'
        self.password = 'firstuserpwd'
        self.user = User.objects.create_user(username=self.username, password=self.password, email='test1@yopmail.com', is_active=True)

        self.username2 = 'seconduser'
        self.password2 = 'seconduserpwd'
        self.user2 = User.objects.create_user(username=self.username2, password=self.password2, email='test2@yopmail.com', is_active=True)


    def test_delete_iban_user(self):
    
        all_permissions = Permission.objects.filter(content_type__app_label='ibanmanage', content_type__model='ibandata')
        #create group
        group = Group.objects.create(name='Ibanadmin')
        # assign permissions
        for permission in all_permissions:
            group.permissions.add(permission)

        self.user.groups.add(group)

        ibanUser1 = Ibandata.objects.create(first_name='fname', last_name='lname', iban='AL47 2121 1009 0000 0002 3569 8741',created_by=self.user)
        
        login = self.client.login(username=self.username, password=self.password)
        deleteuser = self.client.get('/deleteibandata/1/')

        self.assertContains(deleteuser,"Are you sure you want to delete")

    def test_delete_ibanuser_owner(self):
        all_permissions = Permission.objects.filter(content_type__app_label='ibanmanage', content_type__model='ibandata')
        #create group
        group = Group.objects.create(name='Ibanadmin')
        # assign permissions
        for permission in all_permissions:
            group.permissions.add(permission)

        self.user.groups.add(group)
        self.user2.groups.add(group)

        ibanUser1 = Ibandata.objects.create(first_name='fname', last_name='lname', iban='AL47 2121 1009 0000 0002 3569 8741',created_by=self.user)
        ibanUser2 = Ibandata.objects.create(first_name='fname', last_name='lname', iban='AD12 0001 2030 2003 5910 0100',created_by=self.user)
        ibanUser3 = Ibandata.objects.create(first_name='fname', last_name='lname', iban='AT61 1904 3002 3457 3201',created_by=self.user2)

        login = self.client.login(username=self.username, password=self.password)

        updateseconduser = self.client.get('/deleteibandata/3/')
        self.assertContains(updateseconduser,"Forbidden - Error 403")

    def test_delete_ibanuser_notexist(self):
        all_permissions = Permission.objects.filter(content_type__app_label='ibanmanage', content_type__model='ibandata')
        #create group
        group = Group.objects.create(name='Ibanadmin')
        # assign permissions
        for permission in all_permissions:
            group.permissions.add(permission)

        self.user.groups.add(group)
        
        ibanUser1 = Ibandata.objects.create(first_name='fname', last_name='lname', iban='AL47 2121 1009 0000 0002 3569 8741',created_by=self.user)
        ibanUser2 = Ibandata.objects.create(first_name='fname', last_name='lname', iban='AD12 0001 2030 2003 5910 0100',created_by=self.user)
        
        login = self.client.login(username=self.username, password=self.password)

        updateseconduser = self.client.get('/deleteibandata/3/')
        self.assertContains(updateseconduser,"Page Not Found")