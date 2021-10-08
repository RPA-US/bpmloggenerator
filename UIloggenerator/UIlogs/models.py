from django.db import models

import os
import random
from django.db.models.signals import pre_save
from UIloggenerator.utils import unique_slug_generator_title
from django.urls import reverse
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

# Create your models here.

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    new_filename = random.randint(1, 123123123123)
    final_name = f"{new_filename}{ext}"
    return f"UIlogs/{final_name}"

class UIlogQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (
            Q(title__icontains=query)
            | Q(description__icontains=query)
        )
        return self.filter(lookups).distinct()


class UIlogManager(models.Manager):
    def get_queryset(self):
        return UIlogQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(
            id=id
        )  # UIlogs.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)

class UIlog(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)
    description = models.JSONField()
    seed = models.JSONField()
    path = models.TextField()
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Manager
    objects = UIlogManager()

    def get_absolute_url(self):
        return reverse("UIlogs:detail", args=[self.slug])
        # return f"/UIlogs/detail/{self.slug}/"

    def __str__(self):
        return self.title


    def __unicode__(self):
        return self.title

    def create(self, validated_data):
        # usr = self.request.user
        # if (not usr.is_authenticated) or (not usr.role == 2):
        #     raise ValidationError("Provider must be authenticated.")
        # a = validated_data.get("categories")
        # if (not a) or (len(a) == 0):
        #     raise ValidationError("A UIlog has to have at least one associated category")
        validated_data.update({'slug': unique_slug_generator_title(validated_data.get("title"), UIlog)})
        items = validated_data.pop('categories', None)
        action = UIlog.objects.create(**validated_data)
        return action
    class Meta:
        verbose_name = "UIlog"
        verbose_name_plural = "UIlogs"
