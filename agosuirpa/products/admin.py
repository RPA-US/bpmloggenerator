from django.contrib import admin
from .models import Product, ProductsAvailable


class ProductAdmin(admin.ModelAdmin):
    fields = (
        "title",
        "description",
        "price",
        "categories",
        "image",
        "featured",
        "active",
    )
    list_display = ["__str__", "slug"]
    list_filter = ("title", "price")

    class Meta:
        model = Product

class ProductsAvailableAdmin(admin.ModelAdmin):
    pass


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductsAvailable, ProductsAvailableAdmin)
