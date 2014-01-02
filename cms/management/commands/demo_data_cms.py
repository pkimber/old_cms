from django.core.management.base import BaseCommand

from cms.models import Page
from cms.tests.model_maker import make_page


class Command(BaseCommand):

    help = "Create demo data for 'cms'"

    def handle(self, *args, **options):
        try:
            Page.objects.get(slug='home')
        except Page.DoesNotExist:
            make_page('Home', 0)
        try:
            Page.objects.get(slug='information')
        except Page.DoesNotExist:
            make_page('Information', 1)
        try:
            Page.objects.get(slug='portfolio')
        except Page.DoesNotExist:
            make_page('Portfolio', 2)
        print("Created 'cms' demo data...")
