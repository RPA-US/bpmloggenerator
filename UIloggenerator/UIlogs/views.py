from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib import messages

from django.views.generic import ListView, DetailView, CreateView
from .models import UIlog
from .forms import UIlogForm, UIlogActivitiesForm
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
import os, tempfile, zipfile
from wsgiref.util import FileWrapper

# Create your views here.

class UIlogDetailView(DetailView):
    model = UIlog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated and UIlog.objects.filter(user=self.request.user).exists():
            q = UIlog.objects.get(user=self.request.user).UIlogs.all()
            context["hide_button"] = q.filter(pk=kwargs["object"].pk).exists()
        return context

    template_name = "UIlogs/detail.html"


class CreateUIlogView(CreateView):
    model = UIlog
    form_class = UIlogForm
    template_name = "UIlogs/create.html"

    def form_valid(self, form):
        # if not self.request.user.role == 2:
        #     raise ValidationError("Only providers can register UIlogs")
        self.object = UIlog.create(self, form.cleaned_data)
        return render(self.request, "UIlogs/create.html", {"UIlog": self.object})

    def get_initial(self, *args, **kwargs):
        initial = super(CreateUIlogView, self).get_initial(**kwargs)
        # initial['term'] = 'My term'
        return initial

    # def get_form_kwargs(self, *args, **kwargs):
    #     kwargs = super(CreateUIlogView, self).get_form_kwargs(*args, **kwargs)
    #     kwargs['user'] = self.request.user
    #     return kwargs
    
    # def get_context_data(self, **kwargs):
    #     ctx = super(CreateUIlogView, self).get_context_data(**kwargs)
    #     ctx['level_zero'] = [] # context data
    #     return ctx

    
# def varibility_configuration_especification(request, id):
#     uilog = UIlog.objects.get(pk=id)
#     if request.method == "POST":
#         category_term_form = UIlogActivitiesForm(request.POST)
#         report_form = UIlogActivitiesForm(request.POST)
#         if report_form.is_valid() and category_term_form.is_valid():
#             if (not request.user.is_authenticated) or request.user.role != 1:
#                 raise ValidationError("Reviewer must be authenticated.")
#             uilog_validated_data = category_term_form.cleaned_data
#             rep_validated_data = report_form.cleaned_data
#             res = rep_validated_data.get("result")
#             uilog.description = uilog_validated_data.get("description")
#             uilog.categoryChars = uilog_validated_data.get("categoryChars")
#             uilog.formats_supported.clear()
#             uilog.formats_supported.add(
#                 *uilog_validated_data.get("formats_supported")
#             )
#             uilog.decision = uilog_validated_data.get("decision")
#             desc = uilog_validated_data.get("decision")
#             if desc == "1" or desc == "3":
#                 context = {
#                     "report_form": report_form,
#                     "category_term_form": category_term_form,
#                 }
#                 if not res:
#                     messages.warning(
#                         request,
#                         "If the proposal has been accepted it must have a result of that acceptance",
#                     )
#                     return render(request, "categories/create-report.html", context)
               
#             else:
#                 if res:
#                     raise ValidationError(
#                         "The report cannot have a reason for acceptance if the proposal has been rejected"
#                     )

#             uilog.save()

#             return HttpResponseRedirect(
#                 reverse("taxcategs:categoryterm_proposalreview")
#             )
#     else:
#         category_term_form = ProposalReviewForm(instance=uilog)
#         report_form = ReportForm()

#     context = {
#         "reptaxcateg": uilog.substitute_tax_categ,
#         "taxonomicategory": uilog.tax_categ,
#         "report_form": report_form,
#         "category_term_form": category_term_form,
#     }

#     if uilog.image_url:
#         context["cat_image"] = uilog.image

#     return render(request, "categories/create-report.html", context)