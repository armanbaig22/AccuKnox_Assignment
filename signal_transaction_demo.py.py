from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management.base import BaseCommand

class ParentModel(models.Model):
    name = models.CharField(max_length=100)

class ChildModel(models.Model):
    parent = models.ForeignKey(ParentModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

@receiver(post_save, sender=ParentModel)
def create_child(sender, instance, created, **kwargs):
    if created:
        ChildModel.objects.create(parent=instance, name=f"Child of {instance.name}")
        print(f"Child created for {instance.name}")
        # Simulate an error condition
        if instance.name == "ErrorTrigger":
            raise ValueError("Simulated error in signal handler")

class Command(BaseCommand):
    help = 'Demonstrates signal execution in the same transaction as the caller'

    def handle(self, *args, **options):
        # Case 1: Successful transaction
        with transaction.atomic():
            try:
                parent = ParentModel.objects.create(name="Parent1")
                print(f"Parent created: {parent.name}")
                print(f"Child count: {ChildModel.objects.count()}")
            except Exception as e:
                print(f"Error occurred: {str(e)}")

        print(f"Final child count after successful transaction: {ChildModel.objects.count()}")

        # Case 2: Failed transaction
        with transaction.atomic():
            try:
                parent = ParentModel.objects.create(name="ErrorTrigger")
                print(f"Parent created: {parent.name}")
                print(f"Child count: {ChildModel.objects.count()}")
            except Exception as e:
                print(f"Error occurred: {str(e)}")

        print(f"Final child count after failed transaction: {ChildModel.objects.count()}")