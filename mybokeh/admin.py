from django.contrib import admin

# Register your models here.

from .models import myProduct

admin.site.register(myProduct)