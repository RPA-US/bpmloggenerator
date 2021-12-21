import os
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from private_storage.storage.files import PrivateFileSystemStorage
from private_storage.fields import PrivateFileField
from django.shortcuts import get_object_or_404
from .utils import *

class ProductQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(active=True)

    def featured(self):
        return self.filter(featured=True)

    def search(self, query):
        lookups = (
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(price__icontains=query)
            | Q(tag__title__icontains=query)
        )
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(
            id=id
        )  # Products.objects == self.get_queryset()
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)

class Product(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=20, decimal_places=4, default=39.99)
    image = models.ImageField(upload_to=upload_image_path)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # categories = models.ManyToManyField(TaxCateg, limit_choices_to={'active': True})
    user = models.ForeignKey(User, verbose_name="Provider", on_delete=models.CASCADE)
    component = PrivateFileField("Component")

    # Manager
    objects = ProductManager()

    def get_absolute_url(self):
        return reverse("products:detail", args=[self.slug])
        # return f"/products/detail/{self.slug}/"

    def __str__(self):
        return self.title


    def __unicode__(self):
        return self.title

    def create(self, validated_data):
        usr = self.request.user
        if (not usr.is_authenticated) or (not usr.role == 2):
            raise ValidationError("Provider must be authenticated.")
        a = validated_data.get("categories")
        if (not a) or (len(a) == 0):
            raise ValidationError("A product has to have at least one associated category")
        validated_data.update({'user': usr})
        validated_data.update({'slug': unique_slug_generator_title(validated_data.get("title"), Product)})
        items = validated_data.pop('categories', None)
        action = Product.objects.create(**validated_data)
        if items is not None:
            # '*' is the "splat" operator: It takes a list as input, and expands it into actual positional arguments in the function call.
            action.categories.add(*items)
        prodavail_user = ProductsAvailable.objects.filter(user=usr)
        if prodavail_user:
            ls = get_object_or_404(ProductsAvailable, user=usr)
        else:
            ls = ProductsAvailable.objects.create(user=usr)
        ls.products.add(action)
        # ls.save()
        return action
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    # def create_product(
    #     self,
    #     title,
    #     slug,
    #     description,
    #     price,
    #     image,
    #     featured,
    #     active,
    #     categories,
    # ):
    #     a = categories
    #     b = len(categories) == 0
    #     if a or b:
    #         raise ValueError("A product has to have at least one associated category")

    #     prod_obj = self.model(
    #         title=title,
    #         description=description,
    #         price=price,
    #         image=image,
    #         categories=categories,
    #     )
    #     if not slug:
    #         slug2 = unique_slug_generator(self)
    #         prod_obj.set_slug(slug2)
    #     prod_obj.active = is_active
    #     prod_obj.featured = is_featured
    #     prod_obj.save(using=self._db)
    #     return prod_obj

class ProductsAvailable(models.Model):
    products = models.ManyToManyField(Product, verbose_name="Bought products", blank=True)
    user = models.OneToOneField(User, verbose_name="Owner", on_delete=models.CASCADE) 

    class Meta:
        verbose_name = ("ProductsAvailable")
        verbose_name_plural = ("ProductsAvailables")

    def __str__(self):
        return self.user.email

    def get_absolute_url(self):
        return reverse("ProductsAvailable_detail", kwargs={"pk": self.pk})
