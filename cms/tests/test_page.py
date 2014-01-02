from django.test import TestCase

from cms.models import Page
from cms.tests.model_maker import make_page


class TestContent(TestCase):

    def _menu_list_slugs(self):
        return Page.objects.menu().values_list('slug', flat=True)

    def setUp(self):
        self.page = make_page('Home', 0)
        self.page = make_page('Information', 1)
        self.page = make_page('Portfolio', 2)

    def test_menu(self):
        self.assertEqual(2, len(Page.objects.menu()))

    def test_menu_not_home(self):
        self.assertNotIn(
            'home',
            self._menu_list_slugs()
        )

    def test_menu_in(self):
        self.assertIn(
            'information',
            self._menu_list_slugs()
        )
        self.assertIn(
            'portfolio',
            self._menu_list_slugs()
        )
