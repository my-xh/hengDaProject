from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.MyNews)
class MyNewsAdmin(admin.ModelAdmin):
    style_fields = {'description': 'ueditor'}
