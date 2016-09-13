from django.test import TestCase
from django.contrib.sessions.backends.db import SessionStore
from namespaced_session.session import NamespacedSession

# Create your tests here.
class TestNamespacedSession(TestCase):
    def setUp(self):
        self.sess = SessionStore()

    def tearDown(self):
        del self.sess

    def test1(self):
        ns1 = NamespacedSession(self.sess, ['foos', 1, 'bars', 1])
        ns1.update({"bazzes": 1})
        _ns1 = NamespacedSession(self.sess, ['foos', 1, 'bars', 1])
        self.assertEqual(ns1.get_sess_info(), _ns1.get_sess_info())

    def test2(self):
        ns1 = NamespacedSession(self.sess, ['foos', 1, 'bars', 1])
        ns1.update({"bazzes": 1})
        ns2 = NamespacedSession(self.sess, ['foos', 1, 'bars', 2])
        self.assertNotEqual(ns1.get_sess_info(), ns2.get_sess_info())

    def test3(self):
        ns1 = NamespacedSession(self.sess, ['foos', 1, 'bars', 1])
        ns1.update({'bazzes': 1})
        ns2 = NamespacedSession(self.sess, ['foos', 1, 'bars', 2])
        ns2.update({'bazzes': 2})
        ns1.delete()
        self.assertEqual(self.sess.get('foos'),
                         {"1": {"bars": {"2": {"bazzes": 2}}}})

    def test4(self):
        ns1 = NamespacedSession(self.sess, ['foos', 1, 'bars', 1])
        ns1.update({'bazzes': 1})
        ns2 = NamespacedSession(self.sess, ['foos', 1, 'bars', 2])
        ns2.update({'bazzes': 2})
        ns1.delete()
        ns2.delete()
        self.assertIsNone(self.sess.get('foos'))


