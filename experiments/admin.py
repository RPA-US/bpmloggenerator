from django.contrib import admin
from .models import Experiment, Variations

# Register your models here.
admin.site.register(Experiment)
admin.site.register(Variations)
