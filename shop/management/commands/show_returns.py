from django.core.management.base import BaseCommand
from shop.models import Return


class Command(BaseCommand):
    help = "Show all returns"

    def handle(self, *args, **options):
        returns = Return.objects.all()
        for elem in returns:
            self.stdout.write(self.style.ERROR(f"{elem.order} by {elem.create_date}"))
