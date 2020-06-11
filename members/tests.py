from django.test import TestCase
from members.models import *
from unittest.mock import MagicMock
from mxv.nation_builder import NationBuilder

class TestEnsureNationBuilderPerson(TestCase):
    def setUp(self):
        self.nb = MagicMock()
        self.nb.GetFromEmail.return_value = { 
            'id': 999, 
            'email': 'haha@gmail.com', 
            'my_momentum_unique_token': 'aaa'
        }

    ## Naming conventions used in these tests:
    ## c - object created before the test
    ## e - object we're going to ensure
    ## m - object we'll retrieve from the DB and check

    def test_attached(self):
        c = Member.objects.create(email='m@jill.com', name='Correct record')
        NationBuilderPerson.objects.create(nation_builder_id=111, member=c, email=c.email)
        self.nb.PersonFieldsAndValues.return_value = [("email", "m@jill.com")]
        e = Member.objects.get(email='m@jill.com')
        ensure_nationbuilder_person(self.nb, e)
        m = Member.objects.get(email='m@jill.com')
        self.assertEqual(111, m.nation_builder_person.nation_builder_id)
        self.assertEqual(m.nation_builder_person.email, m.email)
        self.nb.GetFromEmail.assert_not_called()
        self.nb.PersonFieldsAndValues.assert_called()

    def test_attached_wrong_id(self):
        c = Member.objects.create(email='nye@bevan.com', name='Bad ID')
        NationBuilderPerson.objects.create(member=c, email=c.email, nation_builder_id=0)
        self.nb.PersonFieldsAndValues.return_value = None
        e = Member.objects.get(email='nye@bevan.com')
        ensure_nationbuilder_person(self.nb, e)
        m = Member.objects.get(email='nye@bevan.com')
        self.assertEqual(999, m.nation_builder_person.nation_builder_id)
        self.assertEqual('haha@gmail.com', m.nation_builder_person.email)
        self.assertEqual('aaa', m.nation_builder_person.unique_token)

    def test_attached_missing_id(self):
        c = Member.objects.create(email='nye@bevan.com', name='Missing ID')
        NationBuilderPerson.objects.create(member=c, email=c.email)
        e = Member.objects.get(email='nye@bevan.com')
        ensure_nationbuilder_person(self.nb, e)
        m = Member.objects.get(email='nye@bevan.com')
        self.assertEqual(999, m.nation_builder_person.nation_builder_id)
        self.assertEqual('haha@gmail.com', m.nation_builder_person.email)
        self.assertEqual('aaa', m.nation_builder_person.unique_token)

    def test_detached(self):
        NationBuilderPerson.objects.create(nation_builder_id=222, email='notmember@gmail.com')
        e = Member.objects.create(email='notmember@gmail.com', name='Just joined')
        ensure_nationbuilder_person(self.nb, e)
        m = Member.objects.get(email='notmember@gmail.com')
        self.assertEqual(222, m.nation_builder_person.nation_builder_id)
        self.assertEqual(m.nation_builder_person.email, m.email)
        self.nb.GetFromEmail.assert_not_called()

    def test_detached_missing_id(self):
        NationBuilderPerson.objects.create(email='notmembernoid@gmail.com')
        e = Member.objects.create(email='notmembernoid@gmail.com', name='Just joined')
        ensure_nationbuilder_person(self.nb, e)
        m = Member.objects.get(email='notmembernoid@gmail.com')
        self.assertEqual(999, m.nation_builder_person.nation_builder_id)
        self.assertEqual('haha@gmail.com', m.nation_builder_person.email)
        self.assertEqual('aaa', m.nation_builder_person.unique_token)

