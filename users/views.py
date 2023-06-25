from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from experiments.views import associate_experiment

# Create your views here.
@receiver(post_save, sender=User)
def create_user_experiment(sender, instance, created, **kwargs):
    if created:
        associate_experiment(user=instance)