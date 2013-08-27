from django.core.management.base import BaseCommand


class Command(BaseCommand):

    help = "Initialise CMS application"

    def handle(self, *args, **options):
        print "Initialised 'cms' app..."
