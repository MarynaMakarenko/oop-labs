import unittest
from app.core.router import Route, Router


class TestRoute(unittest.TestCase):

    def test_static_get_match(self):
        r = Route('GET', '/login', lambda: None)
        self.assertEqual(r.match('GET', '/login'), {})

    def test_method_mismatch(self):
        r = Route('POST', '/login', lambda: None)
        self.assertIsNone(r.match('GET', '/login'))

    def test_parametric_match(self):
        r = Route('GET', '/bookings/:id', lambda: None)
        self.assertEqual(r.match('GET', '/bookings/42'), {'id': '42'})

    def test_parametric_no_partial_match(self):
        r = Route('GET', '/bookings/:id', lambda: None)
        self.assertIsNone(r.match('GET', '/bookings'))
        self.assertIsNone(r.match('GET', '/bookings/42/approve'))

    def test_query_string_ignored(self):
        r = Route('GET', '/rooms', lambda: None)
        self.assertIsNotNone(r.match('GET', '/rooms?page=2'))

    def test_multi_param(self):
        r = Route('GET', '/users/:uid/bookings/:bid', lambda: None)
        result = r.match('GET', '/users/3/bookings/7')
        self.assertEqual(result, {'uid': '3', 'bid': '7'})


class TestRouter(unittest.TestCase):

    def setUp(self):
        self.router = Router()

    def test_dispatch_known_route(self):
        h = lambda ctx, resp: None
        self.router.get('/test', h)
        fn, params = self.router.dispatch('GET', '/test')
        self.assertIs(fn, h)
        self.assertEqual(params, {})

    def test_dispatch_unknown_returns_none(self):
        fn, params = self.router.dispatch('GET', '/missing')
        self.assertIsNone(fn)
        self.assertEqual(params, {})

    def test_dispatch_extracts_path_param(self):
        h = lambda ctx, resp, booking_id: None
        self.router.get('/bookings/:booking_id', h)
        fn, params = self.router.dispatch('GET', '/bookings/99')
        self.assertIs(fn, h)
        self.assertEqual(params['booking_id'], '99')

    def test_get_post_distinct(self):
        gh = lambda: None
        ph = lambda: None
        self.router.get('/items', gh)
        self.router.post('/items', ph)
        self.assertIs(self.router.dispatch('GET',  '/items')[0], gh)
        self.assertIs(self.router.dispatch('POST', '/items')[0], ph)

    def test_first_match_wins(self):
        h1 = lambda: None
        h2 = lambda: None
        self.router.get('/rooms/new', h1)
        self.router.get('/rooms/:id', h2)
        fn, _ = self.router.dispatch('GET', '/rooms/new')
        self.assertIs(fn, h1)


if __name__ == '__main__':
    unittest.main()
