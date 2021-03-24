from django.core.management.base import BaseCommand
from shop.models import Return, Order


class Command(BaseCommand):
    help = "Create two returns"

    def handle(self, *args, **options):
        order = Order.objects.get(id=2)
        ret = Return.objects.create(order=order)
        self.stdout.write(self.style.SUCCESS(f'Successfully added return to order {order.id}'))