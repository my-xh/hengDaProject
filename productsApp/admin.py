from django.contrib import admin
from . import models

# Register your models here.


class ProductImgInline(admin.StackedInline):
    model = models.ProductImg
    extra = 1   # 默认显示条目的数量


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImgInline, ]
