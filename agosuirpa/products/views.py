from django.views.generic import ListView, DetailView, CreateView
from .models import Product, ProductsAvailable
from carts.models import Cart
from .forms import ProductForm
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
import os, tempfile, zipfile
from django.http import HttpResponse, HttpResponseRedirect
from wsgiref.util import FileWrapper
from taxcategs.models import TaxCateg
from django.contrib import messages
from django.urls import reverse
from django.template import loader

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"
    paginate_by = 6

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == 3 and ProductsAvailable.objects.filter(user=self.request.user).exists():
            ps = ProductsAvailable.objects.get(user=self.request.user).products.all()
            q = Product.objects.filter(active=True).exclude(id__in=ps)
        else:
            q = Product.objects.filter(active=True)
        return q

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data()
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        context["level_zero"] = TaxCateg.objects.filter(active=True, level=0).all()
        return context

class LatestProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"
    paginate_by = 6

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == 3 and ProductsAvailable.objects.filter(user=self.request.user).exists():
            ps = ProductsAvailable.objects.get(user=self.request.user).products.all()
            q = Product.objects.filter(active=True).exclude(id__in=ps).order_by("-created_at")
        else:
            q = Product.objects.filter(active=True).order_by("-created_at")
        return q

    def get_context_data(self, *args, **kwargs):
        context = super(LatestProductListView, self).get_context_data()
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context["cart"] = cart_obj
        context["level_zero"] = TaxCateg.objects.filter(active=True, level=0).all()
        return context

class MyProductListView(ListView):
    model = Product
    template_name = "products/my_list.html"
    paginate_by = 50

    def get_queryset(self):
        if self.request.user.is_authenticated and ProductsAvailable.objects.filter(user=self.request.user).exists():
            q = ProductsAvailable.objects.get(user=self.request.user).products.all()
        else:
            q = []
        return q

class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        if self.request.user.is_authenticated and ProductsAvailable.objects.filter(user=self.request.user).exists():
            q = ProductsAvailable.objects.get(user=self.request.user).products.all()
            context["hide_button"] = q.filter(pk=kwargs["object"].pk).exists()
        context["cart"] = cart_obj
        return context

    template_name = "products/detail.html"


class CreateProductView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = "products/create.html"

    def form_valid(self, form):
        if not self.request.user.role == 2:
            raise ValidationError("Only providers can register products")
        self.object = Product.create(self, form.cleaned_data)
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self, *args, **kwargs):
        initial = super(CreateProductView, self).get_initial(**kwargs)
        # initial['term'] = 'My term'
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(CreateProductView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_context_data(self, **kwargs):
        ctx = super(CreateProductView, self).get_context_data(**kwargs)
        ctx['level_zero'] = TaxCateg.objects.filter(active=True, level=0).all()
        return ctx

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

def register_product(request):
    form = ProductForm(request.POST or None)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
    
    if form.is_valid():
        data = form.cleaned_data
        # Checking: user must be a Provider
        if request.user.role == 2:
            slug = data.get("slug")
            title = data.get("title")
            description = data.get("description")
            price = data.get("price")
            image = data.get("image")
            is_featured = data.get("is_featured")
            is_active = data.get("is_active")
            categories = form.data.get("categories")
            new_prod = Product.create_product(
                title,
                slug,
                description,
                price,
                image,
                is_featured,
                is_active,
                categories,
            )
        else:
            new_prod = None
        if new_prod is not None:
            messages.success(request, "Created Product.")
            return reverse("products:detail", kwargs={"slug": self.slug})

        messages.warning(request, "Create Error !")

    context = {"form": form}

    return render(request, "products/create.html", context)

def export_products(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="CRPAsite-components.csv"'

    # products = Product.objects.filter(active=True).order_by('-price')
    products = Product.objects.order_by('-price')
    csv_data = [('Component title', 'Description', 'Price', 'Date of creation', 'Categories')]
    for p in products:
        s = ''.join(p.description.splitlines())
        pp = (p.title,s,p.price,p.created_at, p.categories)
        csv_data.append(pp)

    t = loader.get_template('products/snippets/product-csv.txt')
    c = {'data': csv_data}
    response.write(t.render(c))
    return response