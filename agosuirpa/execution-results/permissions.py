"""
Possible functions for the ``PRIVATE_STORAGE_AUTH_FUNCTION`` setting.
"""
import django
import products.models as Product_model

def allow_staff(private_file):
    b = False
    request = private_file.request
    pa = Product_model.ProductsAvailable.objects.filter(user=request.user)
    p = Product_model.Product.objects.filter(component=private_file.relative_name)
    if pa and p:
        a = p[0]
        b = pa[0].products.filter(pk=a.pk)
    return b and b.exists()
