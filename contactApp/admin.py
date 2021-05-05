from django.contrib import admin
from . import models
from django.utils.safestring import mark_safe

# Register your models here.

@admin.register(models.Ad)
class AdAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'person_id', 'birth', 'edu', 'school',
                  'major', 'position', 'image_data')

    def image_data(self, obj):
        return mark_safe(f'<img src="{obj.photo.url}" width="120px" />')

    image_data.short_description = '个人照片'
