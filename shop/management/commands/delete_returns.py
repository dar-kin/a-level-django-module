from django.core.management.base import BaseCommand
from shop.models import Return


class Command(BaseCommand):
    help = "Delete returns"

    def handle(self, *args, **options):
        Return.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted returns'))