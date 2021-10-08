from django import forms
from .models import UIlog
from django.core.exceptions import ValidationError

# class UIlogForm(forms.ModelForm):
#     class Meta:
#         model = UIlog
#         exclude = ("slug","active","description")
#         fields = (
#             "title",
#         )

#         widgets = {
#             "title": forms.TextInput(
#                 attrs={"class": "form-control", "placeholder": "Title"}
#             ),
#         }

#     def clean_title(self):
#         title = self.cleaned_data.get("title")
#         qs = UIlog.objects.filter(title=title)
#         if qs.exists():
#             raise forms.ValidationError("Title is taken")
#         return title
    
#     def clean_categories(self):
#         cats = self.cleaned_data["categories"]
#         if len(cats) < 1:
#             raise forms.ValidationError(
#                 "A UIlog term cannot have less than one associated category"
#             )
#         return cats

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop("user")
#         super(UIlogForm, self).__init__(*args, **kwargs)


class UIlogForm(forms.ModelForm):
    class Meta:
        model = UIlog
        exclude = ("slug","active","description")
        fields = (
            "title",
            "seed"
        )

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title"}
            ),
            "seed": forms.FileInput(
                attrs={"class": "form-control", "placeholder": "Example log"}
            ),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title")
        qs = UIlog.objects.filter(title=title)
        if qs.exists():
            raise forms.ValidationError("Title is taken")
        return title

    def __init__(self, *args, **kwargs):
        # self.user = kwargs.pop("user")
        super(UIlogForm, self).__init__(*args, **kwargs)



class UIlogActivitiesForm(forms.Form):
    def __init__(self, activities, *args, **kwargs):
        super(UIlog, self).__init__(*args, **kwargs)
        for i in activities:
            self.fields['representative_image_%i' % i] = forms.Charfield()
            self.fields['variate_per_trace_%i' % i] = forms.Charfield()