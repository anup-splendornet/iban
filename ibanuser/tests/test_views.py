from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from autofixture import AutoFixture
from ibanuser.forms import IbanInfoForm
from ibanuser.models import IbanInfo

class HomeViewTestCase(TestCase):
    def setUp(self):
        self.username = 'myuser'
        self.password = 'valid_password1'
        self.client = Client()
        self.url = reverse('home')
        User.objects.create_user(username=self.username, email='email@test.com', is_active=True, password=self.password)

    def test_home_view_redirects_authenticated_user_to_list(self):
        self.client.login(username = self.username, password = self.password)        
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class IBANUserListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('home')
        self.user = AutoFixture(User).create(1)[0]
        fixture = AutoFixture(IbanInfo, field_values = { 'owner': self.user })
        self.ibanusers = fixture.create(10)

    def test_iban_list_lists_all_users(self):        
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(self.ibanusers), len(response.context['ibanusers']))

    def test_ibanuser_list_displays_users_ibanuser_only(self):
        other_user = AutoFixture(User).create(1)[0]
        AutoFixture(IbanInfo, field_values = { 'owner': other_user }).create(1)
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(self.ibanusers), len(response.context['ibanusers']))


class CreateIbanUserViewTestCase(TestCase):    
    def setUp(self):
        self.client = Client()
        self.url = reverse('adduser')
        self.user = AutoFixture(User).create(1)[0]

    def test_create_ibanuser_always_forces_user(self):
        other_user = AutoFixture(User).create(1)[0]
        self.client.force_login(self.user)

        self.client.post(self.url, {
        'first_name': 'abc',
        'last_name': 'xyz',
        'iban': 'HR12 1001 0051 8630 0016 0',     
        'owner': other_user.id
        }, follow = True)

        self.assertIsNotNone(IbanInfo.objects.first())
        self.assertEqual(IbanInfo.objects.first().owner, self.user)

class IbanUserUpdateViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = AutoFixture(User).create(1)[0]
        self.ibanuser = AutoFixture(IbanInfo, field_values = { 'owner': self.user }).create(1)[0]
        self.url = reverse('edituser', args = [self.ibanuser.id])

    def test_ibanuser_view_shows_update_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed('ibanuser/ibaninfo.html')
        self.assertEqual(IbanInfoForm, response.context['form'].__class__)
        self.assertTrue(response.context['update'])


class IbanUserDeleteViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = AutoFixture(User).create(1)[0]
        self.ibanuser = AutoFixture(IbanInfo, field_values = { 'owner': self.user }).create(1)[0]               
        self.url = reverse('deleteuser', args = [self.ibanuser.id])

    def test_ibanuser_view_shows_delete_form(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertTemplateUsed('ibanuser/ibaninfo_confirm_delete.html')
        self.assertTrue(response.context['delete'])
