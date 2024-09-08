import time
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.management.base import BaseCommand

class MyModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, created, **kwargs):
    print(f"Signal handler started for: {instance.name}")
    time.sleep(2)  # Simulate some time-consuming operation
    print(f"Signal handler finished for: {instance.name}")

class Command(BaseCommand):
    help = 'Demonstrates synchronous signal execution'

    def handle(self, *args, **options):
        print("Starting object creation...")
        start_time = time.time()

        obj = MyModel.objects.create(name="Test Object")

        end_time = time.time()
        print(f"Object created. Name: {obj.name}")
        print(f"Total execution time: {end_time - start_time:.2f} seconds")