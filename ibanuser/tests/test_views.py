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
        self.assertEqual(len(self.ibanusers), len(response.context['userdetails']))

    def test_ibanuser_list_displays_users_ibanuser_only(self):
        other_user = AutoFixture(User).create(1)[0]
        AutoFixture(IbanInfo, field_values = { 'owner': other_user }).create(1)
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(len(self.ibanusers), len(response.context['userdetails']))


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

