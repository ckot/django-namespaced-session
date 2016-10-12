from django.test import TestCase
from django.contrib.sessions.backends.db import SessionStore
from namespaced_session.session import NamespacedSession

# Create your tests here.
class TestNamespacedSession(TestCase):
    def setUp(self):
        self.session = SessionStore()

    def tearDown(self):
        del self.session


    def test_set_empty_dict(self):
        """tests that set() method properly modifies dict"""
        nss = NamespacedSession(self, ['foos', 1, 'bars', 1])
        nss.set(["baz", 1, "boo"], 2)
        sess_info = nss.get_sess_info()
        self.assertEqual(sess_info, {"baz": {'1': {"boo": 2}}})

    def test_get(self):
        nss = NamespacedSession(self, ['foos', 1, 'bars', 1])
        nss.set(["baz", 1, "boo"], 2)
        boo_val = nss.get(["baz", 1, "boo"])
        self.assertEqual(boo_val, 2)

    def test_set_non_empty_dict(self):
        nss = NamespacedSession(self, ['foos', 1, 'bars', 1])
        nss.set(["baz", 1, "boo"], 2)
        nss.set(["baz", 1, "boo"], 3)
        sess_info = nss.get_sess_info()
        boo_val = nss.get(["baz", 1, "boo"])
        self.assertEqual(boo_val, 3)

    def test_update_empty_dict(self):
        nss = NamespacedSession(self, ['foos', 1, 'bars', 1])
        nss.update({"bazzes": 1})
        sess_info = nss.get_sess_info()
        self.assertEqual(sess_info, {"bazzes": 1})

    def test_update_non_empty_dict(self):
        nss = NamespacedSession(self, ['foos', 1, 'bars', 1])
        nss.set(["baz", 1, "boo"], 2)
        nss.update({"bazzes": 1})
        sess_info = nss.get_sess_info()
        self.assertEqual(sess_info, {
            'baz': {'1': {'boo': 2}},
            'bazzes': 1})

    def test_clear(self):
        nss = NamespacedSession(self, ['foos', 1, 'bars', 1])
        nss.set(["baz", 1, "boo"], 2)
        nss.clear()
        sess_info = nss.get_sess_info()
        self.assertEqual(sess_info, {})

    def test_delete_path_len_1(self):
        nss = NamespacedSession(self, ['foos', 1, 'bars', 1])
        nss.set(["baz", 1, "boo"], 2)
        nss.delete(["baz"])
        sess_info = nss.get_sess_info()
        self.assertEqual(sess_info, {})

    def test_delete_path_len_gt_1(self):
        nss = NamespacedSession(self, ['foos', 1, 'bars', 1])
        nss.set(["baz", 1, "boo"], 2)
        nss.delete(["baz", 1, "boo"])
        sess_info = nss.get_sess_info()
        self.assertEqual(sess_info, {"baz": {"1": {}}})

    def test_destroy_deletes_all_paths(self):
        nss = NamespacedSession(self, ['foos', 1, 'bars', 1])
        nss.set(["baz", 1, "boo"], 2)
        nss.delete(["baz", 1, "boo"])
        sess_info = nss.get_sess_info()
        self.assertEqual(sess_info, {"baz": {"1": {}}})

    def test_same_paths_same_dict(self):
        # both session have the same path, and thus should have the
        # same dictionary
        ns1 = NamespacedSession(self, ['foos', 1, 'bars', 1])
        ns1.update({"bazzes": 1})
        _ns1 = NamespacedSession(self, ['foos', 1, 'bars', 1])
        self.assertEqual(ns1.get_sess_info(), _ns1.get_sess_info())

    def test_diff_paths_diff_dicts(self):
        # sessions have different paths, and thus different dictionaries
        ns1 = NamespacedSession(self, ['foos', 1, 'bars', 1])
        ns1.update({"bazzes": 1})
        ns2 = NamespacedSession(self, ['foos', 1, 'bars', 2])
        self.assertNotEqual(ns1.get_sess_info(), ns2.get_sess_info())

    def test_destroy_preserves_other_paths(self):
        # after destroying foos.1.bars.1  foos should only contain
        # foos.1.bars.2 and it's dict
        ns1 = NamespacedSession(self, ['foos', 1, 'bars', 1])
        ns1.update({'bazzes': 1})
        ns2 = NamespacedSession(self, ['foos', 1, 'bars', 2])
        ns2.update({'bazzes': 2})
        ns1.destroy()
        self.assertEqual(self.session.get('foos'),
                         {"1": {"bars": {"2": {"bazzes": 2}}}})

    def test_destroy_deletes_all_paths(self):
        # deleting both paths also deletes session.foos
        ns1 = NamespacedSession(self, ['foos', 1, 'bars', 1])
        ns1.update({'bazzes': 1})
        ns2 = NamespacedSession(self, ['foos', 1, 'bars', 2])
        ns2.update({'bazzes': 2})
        ns1.destroy()
        ns2.destroy()
        self.assertIsNone(self.session.get('foos'))


