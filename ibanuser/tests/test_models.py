from django.test import TestCase
from ibanuser.models import IbanInfo
from django.test import TransactionTestCase
from django.utils import timezone

class IbanModelTransactionTestCase(TransactionTestCase):
    fixtures = ['ibanuser/fixtures/unit-test.json']

    def test_fixtures_load(self):
        self.assertTrue(IbanInfo.objects.count() > 0)


class IbanInfoModelTestCase(TestCase):
    
    def test_object_name_is_first_name_space_last_name(self):
        ibaninfo=IbanInfo()
        expected_object_name = '%s %s' % (ibaninfo.first_name, ibaninfo.last_name)
        self.assertEquals(expected_object_name,str(ibaninfo))

