import time
import unittest
from app.core.session import Session, SessionManager


class TestSession(unittest.TestCase):

    def test_valid_session(self):
        s = Session('id1', time.time() + 3600)
        self.assertTrue(s.is_valid())

    def test_expired_session(self):
        s = Session('id1', time.time() - 1)
        self.assertFalse(s.is_valid())

    def test_get_set(self):
        s = Session('id1', time.time() + 3600)
        s.set('user_id', 7)
        self.assertEqual(s.get('user_id'), 7)

    def test_get_missing_default(self):
        s = Session('id1', time.time() + 3600)
        self.assertIsNone(s.get('nope'))
        self.assertEqual(s.get('nope', 42), 42)

    def test_remove_key(self):
        s = Session('id1', time.time() + 3600)
        s.set('x', 1)
        s.remove('x')
        self.assertIsNone(s.get('x'))


class TestSessionManager(unittest.TestCase):

    def setUp(self):
        self.mgr = SessionManager()

    def test_create_returns_session(self):
        s = self.mgr.create()
        self.assertIsNotNone(s.id)
        self.assertTrue(s.is_valid())

    def test_get_existing(self):
        s = self.mgr.create()
        retrieved = self.mgr.get(s.id)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.id, s.id)

    def test_get_missing(self):
        self.assertIsNone(self.mgr.get('no-such-id'))

    def test_destroy(self):
        s = self.mgr.create()
        self.mgr.destroy(s.id)
        self.assertIsNone(self.mgr.get(s.id))

    def test_data_persists(self):
        s = self.mgr.create()
        s.set('role', 'admin')
        self.assertEqual(self.mgr.get(s.id).get('role'), 'admin')

    def test_set_cookie_contains_id(self):
        cookie = SessionManager.set_cookie('test-session-id')
        self.assertIn('test-session-id', cookie)

    def test_clear_cookie_max_age_zero(self):
        cookie = SessionManager.clear_cookie()
        self.assertIn('max-age=0', cookie.lower())


if __name__ == '__main__':
    unittest.main()
