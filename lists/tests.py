from django.test import TestCase

class BadTest(TestCase):
    def test_fakeee(self):
        self.assertEqual(1, 2)

        
