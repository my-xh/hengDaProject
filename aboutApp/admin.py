from django.contrib import admin
from . import models

# Register your models here.


@admin.register(models.Award)
class AwardAdmin(admin.ModelAdmin):
    list_display = ['description', 'photo']

admin.AdminSite.site_header = '企业门户网站后台管理系统'
admin.AdminSite.site_title = '企业门户网站后台管理系统'
# admin.AdminSite.index_title = '首页'