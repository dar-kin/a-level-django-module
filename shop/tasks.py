from celery import shared_task
from shop.models import Return


@shared_task
def approve_all_returns():
    ret = Return.objects.all()
    for elem in ret:
        elem.delete(approved=True)
    return "Returns were successfully approved"


@shared_task
def delete_all_returns():
    Return.objects.all().delete()
