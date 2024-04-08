# myapp/management/commands/my_custom_command.py

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'My custom Django management command'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Successfully ran my_custom_command'))