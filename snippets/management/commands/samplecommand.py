from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        iso = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        tzinfo = now.tzinfo
        self.stdout.write(f'timezone.now(): {iso}, tzinfo: {tzinfo}')
        print(f'timezone.now(): {iso}, tzinfo: {tzinfo}')
