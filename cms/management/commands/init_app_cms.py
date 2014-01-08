from django.core.management.base import BaseCommand

from cms.tests.scenario import default_moderate_state


class Command(BaseCommand):

    help = "Initialise CMS application"

    def handle(self, *args, **options):
        default_moderate_state()
        print "Initialised 'cms' app..."
