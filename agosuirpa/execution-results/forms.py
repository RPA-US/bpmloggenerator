from django import forms
from .models import Product
from taxcategs import models as tax_categ
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ("slug","active",)
        fields = (
            "title",
            "description",
            "price",
            "categories",
            "image",
            "component",
            "featured",
        )

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title"}
            ),
            "description": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Description"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Price"}
            ),
            "image": forms.FileInput(
                attrs={"class": "form-control", "placeholder": "Image"}
            ),
            "component": forms.FileInput(
                attrs={"class": "form-control", "placeholder": "File"}
            ),
            "featured": forms.CheckboxInput(
                attrs={"class": "primary-checkbox", "checked": "checked"}
            ),
            "categories": forms.SelectMultiple(
                attrs={
                    "class": "multipleselector",
                    "data-placeholder": "Click to select an option...",
                    "multiple": "multiple",
                }
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        qs = Product.objects.filter(title=title)
        if qs.exists():
            raise forms.ValidationError("Title is taken")
        return title
    
    def clean_categories(self):
        cats = self.cleaned_data["categories"]
        if len(cats) < 1:
            raise forms.ValidationError(
                "A product term cannot have less than one associated category"
            )
        return cats

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super(ProductForm, self).__init__(*args, **kwargs)