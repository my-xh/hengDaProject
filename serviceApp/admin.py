from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Doc)
class DocAdmin(admin.ModelAdmin):
    pass
