from django.core.management.base import BaseCommand

from cms.tests.model_maker import make_section


class Command(BaseCommand):

    help = "Create demo data for 'cms'"

    def handle(self, *args, **options):
        make_section('home')
        make_section('portfolio')
        make_section('tech')
        print("Created 'cms' demo data...")
