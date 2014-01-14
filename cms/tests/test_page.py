from django.test import TestCase

from cms.models import Page
from cms.tests.model_maker import make_page


class TestContent(TestCase):

    def setUp(self):
        self.page = make_page('Home', 0)
        self.page = make_page('Information', 1)
        self.page = make_page('Portfolio', 2)

    def test_menu(self):
        self.assertEqual(3, len(Page.objects.menu()))

    def test_menu_in(self):
        result = [p.slug for p in Page.objects.menu()]
        self.assertListEqual(
            ['home', 'information', 'portfolio'],
            result
        )
