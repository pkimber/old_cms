from django.core.management.base import BaseCommand

from cms.tests.model_maker import make_page


class Command(BaseCommand):

    help = "Create demo data for 'cms'"

    def handle(self, *args, **options):
        make_page('home')
        make_page('portfolio')
        make_page('tech')
        print("Created 'cms' demo data...")
