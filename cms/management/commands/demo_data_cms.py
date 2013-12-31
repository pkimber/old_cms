from django.core.management.base import BaseCommand

from cms.models import Page
from cms.tests.model_maker import make_page


class Command(BaseCommand):

    help = "Create demo data for 'cms'"

    def handle(self, *args, **options):
        try:
            Page.objects.get(name='home')
        except Page.DoesNotExist:
            make_page('home')
        try:
            Page.objects.get(name='portfolio')
        except Page.DoesNotExist:
            make_page('portfolio')
        try:
            Page.objects.get(name='tech')
        except Page.DoesNotExist:
            make_page('tech')
        print("Created 'cms' demo data...")
