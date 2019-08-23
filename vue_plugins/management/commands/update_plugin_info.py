from django.core.management import BaseCommand

from vue_plugins.jobs import update_plugins_info
from vue_plugins.models import VuePlugin


class Command(BaseCommand):
    help = 'Updates all plugins in the database with the latest info from github and npm'

    def handle(self, *args, **options):

        plugins = VuePlugin.objects.all()
        results = update_plugins_info(list(plugins))
        self.stdout.write(self.style.SUCCESS(results))